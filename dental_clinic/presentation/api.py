"""Presentation Layer (рівень 3) — FastAPI та Swagger (/docs)."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from data_access import init_db, get_session, Patient
from presentation.controllers import run_import_from_data_folder


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Dental Clinic API",
    description="Стоматологічна клініка — 3 шари: presentation → business → data_access. Swagger: /docs",
    version="1.0.0",
    lifespan=lifespan,
)


def get_db() -> Session:
    db = get_session()
    try:
        yield db
    finally:
        db.close()


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
