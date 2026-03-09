from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    id: str
    family_name: str
    given_name: str
    gender: str
    birthDate: date
    identification_doc: str
    weight: str
    height: str
    medical_summary: str

    @validator("gender")
    def validate_gender(cls, v):
        if v not in ["male", "female", "other"]:
            raise ValueError("Género inválido")
        return v

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    family_name: str | None = None
    given_name: str | None = None
    gender: str | None = None
    birthDate: date | None = None
    identification_doc: str | None = None
    weight: str | None = None
    height: str | None = None
    medical_summary: str | None = None

class PatientResponse(BaseModel):
    id: str
    family_name: str
    given_name: str
    gender: str
    birthDate: date
    identification_doc: str
    weight: str
    height: str
    medical_summary: str

    class Config:
        from_attributes = True


class ObservationBase(BaseModel):
    patient_id: str
    category: str
    code: str
    display: str
    value: float
    unit: str
    date: date

class ObservationCreate(ObservationBase):
    pass

class ObservationResponse(ObservationBase):
    id: str

    class Config:
       from_attributes = True