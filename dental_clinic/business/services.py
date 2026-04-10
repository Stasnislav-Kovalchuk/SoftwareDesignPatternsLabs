"""Business Layer (рівень 2) — імпорт CSV, валідація, збереження через репозиторії."""
import csv
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List, Tuple, Optional

from data_access import (
    get_session,
    init_db,
    reset_db,
    Patient,
    Dentist,
    Appointment,
    Visit,
    Diagnosis,
    TreatmentPlan,
    DentalProcedure,
    Payment,
    PatientRepository,
    DentistRepository,
    AppointmentRepository,
    VisitRepository,
    DiagnosisRepository,
    TreatmentPlanRepository,
    DentalProcedureRepository,
    PaymentRepository,
)

DEFAULT_SPECIALTY = "General"


def _parse_decimal(value: str) -> Decimal:
    if not value or not value.strip():
        return Decimal("0")
    try:
        return Decimal(value.strip().replace(",", "."))
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _parse_date(value: str) -> Optional[datetime]:
    if not value or not value.strip():
        return None
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def _validate_row(row: dict) -> Tuple[bool, str]:
    for key in ("patient_first_name", "patient_last_name", "patient_phone", "patient_email", "dentist_name", "appointment_date"):
        if not row.get(key, "").strip():
            return False, f"Missing: {key}"
    if _parse_date(row.get("appointment_date", "")) is None:
        return False, "Invalid date"
    return True, ""


def import_csv(file_path: Path) -> Tuple[int, int, List[str]]:
    """Читає CSV, створює об'єкти, уникає дублікатів пацієнтів, зберігає. Повертає (processed, failed, errors)."""
    init_db()
    session = get_session()
    prepo = PatientRepository(session)
    drepo = DentistRepository(session)
    arepo = AppointmentRepository(session)
    vrepo = VisitRepository(session)
    diag_repo = DiagnosisRepository(session)
    plan_repo = TreatmentPlanRepository(session)
    proc_repo = DentalProcedureRepository(session)
    pay_repo = PaymentRepository(session)

    processed, failed, errors = 0, 0, []
    if not file_path.exists():
        return 0, 0, [f"File not found: {file_path}"]

    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return 0, 0, ["CSV has no headers"]
            for row_num, row in enumerate(reader, start=2):
                ok, err = _validate_row(row)
                if not ok:
                    failed += 1
                    errors.append(f"Row {row_num}: {err}")
                    continue
                try:
                    dt = _parse_date(row["appointment_date"])
                    if dt is None:
                        failed += 1
                        errors.append(f"Row {row_num}: Invalid date")
                        continue
                    patient = prepo.find_or_create(
                        row["patient_first_name"].strip(),
                        row["patient_last_name"].strip(),
                        row["patient_phone"].strip(),
                        row["patient_email"].strip(),
                    )
                    dentist = drepo.find_or_create(row["dentist_name"].strip(), DEFAULT_SPECIALTY)
                    app = Appointment(appointment_date=dt, patient_id=patient.id, dentist_id=dentist.id)
                    arepo.add(app)
                    visit = Visit(visit_date=dt, notes="", appointment_id=app.id)
                    vrepo.add(visit)
                    if row.get("diagnosis", "").strip():
                        diag_repo.add(Diagnosis(description=row["diagnosis"].strip(), visit_id=visit.id))
                    if row.get("treatment_plan", "").strip():
                        plan_repo.add(TreatmentPlan(plan_description=row["treatment_plan"].strip(), visit_id=visit.id))
                    if row.get("procedure_name", "").strip():
                        proc_repo.add(DentalProcedure(
                            name=row["procedure_name"].strip(),
                            cost=_parse_decimal(row.get("procedure_cost", "0")),
                            visit_id=visit.id,
                        ))
                    pay_repo.add(Payment(amount=_parse_decimal(row.get("payment_amount", "0")), payment_date=dt, visit_id=visit.id))
                    processed += 1
                except Exception as e:
                    failed += 1
                    errors.append(f"Row {row_num}: {e!s}")
        session.commit()
    except Exception as e:
        session.rollback()
        errors.append(f"Import failed: {e!s}")
    finally:
        session.close()

    return processed, failed, errors


def run_import(csv_path: Path) -> dict:
    processed, failed, errors = import_csv(csv_path)
    return {"processed": processed, "failed": failed, "total_rows": processed + failed, "errors": errors}


def run_reset_and_import(csv_path: Path) -> dict:
    """Очистити БД і виконати імпорт заново (щоб в адмінці було видно нові дані)."""
    reset_db()
    return run_import(csv_path)
