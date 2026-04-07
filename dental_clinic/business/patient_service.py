"""Business Layer — CRUD сервіс для основної сутності Patient (MVC Model logic)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from sqlalchemy.exc import IntegrityError

from data_access.models import Patient
from data_access.repositories import PatientRepository


@dataclass(frozen=True)
class PatientCreate:
    first_name: str
    last_name: str
    phone: str
    email: str


@dataclass(frozen=True)
class PatientUpdate:
    first_name: str
    last_name: str
    phone: str
    email: str


class PatientService:
    """
    Бізнес-логіка для Patient.
    Контролери не працюють напряму з БД — тільки через цей сервіс.
    """

    def __init__(self, repo: PatientRepository):
        self._repo = repo

    def list(self, limit: int = 50, offset: int = 0) -> List[Patient]:
        return self._repo.list_patients(limit=limit, offset=offset)

    def count(self) -> int:
        return self._repo.count()

    def get(self, patient_id: int) -> Optional[Patient]:
        return self._repo.get_by_id(patient_id)

    def create(self, data: PatientCreate) -> Patient:
        patient = Patient(
            first_name=data.first_name.strip(),
            last_name=data.last_name.strip(),
            phone=data.phone.strip(),
            email=data.email.strip(),
        )
        self._repo.add(patient)
        try:
            self._repo._s.commit()  # транзакція на рівні сервісу
        except IntegrityError:
            self._repo._s.rollback()
            raise
        return patient

    def update(self, patient_id: int, data: PatientUpdate) -> Optional[Patient]:
        patient = self._repo.get_by_id(patient_id)
        if patient is None:
            return None
        patient.first_name = data.first_name.strip()
        patient.last_name = data.last_name.strip()
        patient.phone = data.phone.strip()
        patient.email = data.email.strip()
        self._repo.update(patient)
        try:
            self._repo._s.commit()
        except IntegrityError:
            self._repo._s.rollback()
            raise
        return patient

    def delete(self, patient_id: int) -> bool:
        patient = self._repo.get_by_id(patient_id)
        if patient is None:
            return False
        self._repo.delete(patient)
        self._repo._s.commit()
        return True

