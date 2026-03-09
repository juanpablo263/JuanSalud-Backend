from sqlalchemy import Column, String, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # admin, medico, paciente
    access_key = Column(String, nullable=False)
    permission_key = Column(String, unique=True, nullable=False)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    family_name = Column(String, nullable=False)
    given_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birthDate = Column(Date, nullable=False)
    identification_doc = Column(String, nullable=False) 
    weight = Column (String,nullable=False)
    height = Column (String,nullable=False)
    medical_summary = Column(String, nullable=False)    

    observations = relationship("Observation", back_populates="patient", cascade="all, delete")


class Observation(Base):
    __tablename__ = "observations"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)

    category = Column(String, nullable=False)
    code = Column(String, nullable=False)
    display = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    patient = relationship("Patient", back_populates="observations")