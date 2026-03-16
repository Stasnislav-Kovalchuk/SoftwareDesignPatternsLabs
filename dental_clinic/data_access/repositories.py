"""Data Access Layer — репозиторії."""
from typing import Optional
from sqlalchemy.orm import Session

from data_access.models import (
    Patient, Dentist, Appointment, Visit,
    Diagnosis, TreatmentPlan, DentalProcedure, Payment,
)


class PatientRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, patient: Patient) -> Patient:
        self._s.add(patient)
        self._s.flush()
        return patient

    def get_by_email(self, email: str) -> Optional[Patient]:
        return self._s.query(Patient).filter(Patient.email == email).first()

    def get_all(self) -> list[Patient]:
        """Повертає всіх пацієнтів (зручно для простих перевірок/тестів)."""
        return self._s.query(Patient).all()

    def find_or_create(self, first_name: str, last_name: str, phone: str, email: str) -> Patient:
        p = self.get_by_email(email)
        if p:
            return p
        return self.add(Patient(first_name=first_name, last_name=last_name, phone=phone, email=email))


class DentistRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, dentist: Dentist) -> Dentist:
        self._s.add(dentist)
        self._s.flush()
        return dentist

    def get_by_name(self, name: str) -> Optional[Dentist]:
        return self._s.query(Dentist).filter(Dentist.name == name).first()

    def find_or_create(self, name: str, specialty: str) -> Dentist:
        d = self.get_by_name(name)
        if d:
            return d
        return self.add(Dentist(name=name, specialty=specialty))


class AppointmentRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, appointment: Appointment) -> Appointment:
        self._s.add(appointment)
        self._s.flush()
        return appointment


class VisitRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, visit: Visit) -> Visit:
        self._s.add(visit)
        self._s.flush()
        return visit


class DiagnosisRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, diagnosis: Diagnosis) -> Diagnosis:
        self._s.add(diagnosis)
        self._s.flush()
        return diagnosis


class TreatmentPlanRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, plan: TreatmentPlan) -> TreatmentPlan:
        self._s.add(plan)
        self._s.flush()
        return plan


class DentalProcedureRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, procedure: DentalProcedure) -> DentalProcedure:
        self._s.add(procedure)
        self._s.flush()
        return procedure


class PaymentRepository:
    def __init__(self, session: Session):
        self._s = session

    def add(self, payment: Payment) -> Payment:
        self._s.add(payment)
        self._s.flush()
        return payment
