# Data Access Layer (рівень 1)
from data_access.database import Base, get_engine, get_session, init_db, reset_db
from data_access.models import (
    Patient, Dentist, Appointment, Visit,
    Diagnosis, TreatmentPlan, DentalProcedure, Payment,
)
from data_access.repositories import (
    PatientRepository, DentistRepository, AppointmentRepository, VisitRepository,
    DiagnosisRepository, TreatmentPlanRepository, DentalProcedureRepository, PaymentRepository,
)
