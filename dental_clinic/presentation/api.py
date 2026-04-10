"""Presentation Layer (рівень 3) — FastAPI (Swagger + MVC HTML Views)."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Depends, Form, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from data_access import init_db, get_session, Patient
from data_access.repositories import PatientRepository
from business.patient_service import PatientService, PatientCreate, PatientUpdate
from presentation.controllers import run_import_from_data_folder, run_reset_import_from_data_folder


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Dental Clinic API",
    description="Стоматологічна клініка — MVC (HTML) + API. 3 шари: presentation → business → data_access. Swagger: /docs",
    version="1.0.0",
    lifespan=lifespan,
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


def get_db() -> Session:
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def get_patient_service(db: Session = Depends(get_db)) -> PatientService:
    """IoC/DI: створення сервісу з репозиторієм, прив’язаним до session."""
    return PatientService(PatientRepository(db))


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str


class ImportResult(BaseModel):
    processed: int
    failed: int
    total_rows: int
    errors: List[str]


@app.get("/patients", response_model=List[PatientRead])
def list_patients(db: Session = Depends(get_db)):
    """Список пацієнтів."""
    return db.query(Patient).all()


@app.post("/import", response_model=ImportResult)
def import_csv_endpoint():
    """Імпорт з data/dental_data.csv."""
    result = run_import_from_data_folder()
    return ImportResult(**result)


@app.post("/import/reset", response_model=ImportResult)
def reset_and_import_csv_endpoint():
    """Очистити БД і імпортувати CSV заново (щоб бачити нові дані після генерації)."""
    result = run_reset_import_from_data_folder()
    return ImportResult(**result)


# ---------------- MVC HTML Views (Lab 3) ----------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse(url="/ui/patients", status_code=302)


@app.get("/ui/patients", response_class=HTMLResponse)
def patients_page(
    request: Request,
    service: PatientService = Depends(get_patient_service),
):
    limit = int(Query(50, ge=1, le=500).default)  # fallback, overwritten below
    offset = int(Query(0, ge=0).default)
    # Беремо з query params вручну, щоб не “засмічувати” сигнатуру шаблонними Query-обʼєктами в документації.
    try:
        limit = max(1, min(500, int(request.query_params.get("limit", "50"))))
    except ValueError:
        limit = 50
    try:
        offset = max(0, int(request.query_params.get("offset", "0")))
    except ValueError:
        offset = 0

    total = service.count()
    patients = service.list(limit=limit, offset=offset)
    prev_offset = max(0, offset - limit)
    next_offset = offset + limit
    return templates.TemplateResponse(
        name="patients_list.html",
        request=request,
        context={
            "patients": patients,
            "total": total,
            "limit": limit,
            "offset": offset,
            "prev_offset": prev_offset,
            "next_offset": next_offset,
        },
    )


@app.get("/ui/patients/new", response_class=HTMLResponse)
def patient_new_form(request: Request):
    return templates.TemplateResponse(
        name="patient_form.html",
        request=request,
        context={"mode": "create", "patient": None, "error": None},
    )


@app.post("/ui/patients/new")
def patient_create(
    service: PatientService = Depends(get_patient_service),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
):
    service.create(PatientCreate(first_name=first_name, last_name=last_name, phone=phone, email=email))
    return RedirectResponse(url="/ui/patients", status_code=303)


@app.get("/ui/patients/{patient_id}/edit", response_class=HTMLResponse)
def patient_edit_form(
    request: Request,
    patient_id: int,
    service: PatientService = Depends(get_patient_service),
):
    patient = service.get(patient_id)
    if patient is None:
        return templates.TemplateResponse(
            name="error.html",
            request=request,
            context={"message": "Пацієнта не знайдено"},
            status_code=404,
        )
    return templates.TemplateResponse(
        name="patient_form.html",
        request=request,
        context={"mode": "edit", "patient": patient, "error": None},
    )


@app.post("/ui/patients/{patient_id}/edit")
def patient_update(
    patient_id: int,
    service: PatientService = Depends(get_patient_service),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
):
    updated = service.update(
        patient_id,
        PatientUpdate(first_name=first_name, last_name=last_name, phone=phone, email=email),
    )
    if updated is None:
        return RedirectResponse(url="/ui/patients", status_code=303)
    return RedirectResponse(url="/ui/patients", status_code=303)


@app.post("/ui/patients/{patient_id}/delete")
def patient_delete(
    patient_id: int,
    service: PatientService = Depends(get_patient_service),
):
    service.delete(patient_id)
    return RedirectResponse(url="/ui/patients", status_code=303)
