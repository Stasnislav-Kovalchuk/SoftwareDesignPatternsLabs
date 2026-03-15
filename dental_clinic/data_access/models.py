"""Data Access Layer — ORM моделі."""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship

from data_access.database import Base


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    appointments = relationship("Appointment", back_populates="patient")


class Dentist(Base):
    __tablename__ = "dentists"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    specialty = Column(String(100), nullable=False)
    appointments = relationship("Appointment", back_populates="dentist")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_date = Column(DateTime, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("dentists.id"), nullable=False)
    patient = relationship("Patient", back_populates="appointments")
    dentist = relationship("Dentist", back_populates="appointments")
    visit = relationship("Visit", back_populates="appointment", uselist=False)


class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    appointment = relationship("Appointment", back_populates="visit")
    diagnoses = relationship("Diagnosis", back_populates="visit", cascade="all, delete-orphan")
    treatment_plan = relationship("TreatmentPlan", back_populates="visit", uselist=False, cascade="all, delete-orphan")
    dental_procedures = relationship("DentalProcedure", back_populates="visit", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="visit", uselist=False, cascade="all, delete-orphan")


class Diagnosis(Base):
    __tablename__ = "diagnoses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    visit = relationship("Visit", back_populates="diagnoses")


class TreatmentPlan(Base):
    __tablename__ = "treatment_plans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_description = Column(Text, nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    visit = relationship("Visit", back_populates="treatment_plan")


class DentalProcedure(Base):
    __tablename__ = "dental_procedures"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    visit = relationship("Visit", back_populates="dental_procedures")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=False)
    visit = relationship("Visit", back_populates="payment")
