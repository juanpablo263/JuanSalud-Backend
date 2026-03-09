from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import verify_access_key, require_role
from app.crypto import encrypt, decrypt
from app.limiter import limiter

router = APIRouter(
    prefix="/JuanSalud/Patient",
    tags=["Patient"],
    dependencies=[Depends(verify_access_key)]
)

def desencriptar_paciente(patient):
    patient.identification_doc = decrypt(patient.identification_doc)
    patient.medical_summary = decrypt(patient.medical_summary)
    return patient

@router.post("/", response_model=schemas.PatientResponse)
@limiter.limit("20/minute")
def create_patient(
    request: Request,
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico"))
):
    existing = db.query(models.Patient).filter(models.Patient.id == patient.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="El paciente ya existe")

    data = patient.dict()
    data["identification_doc"] = encrypt(data["identification_doc"])  # ← encripta
    data["medical_summary"] = encrypt(data["medical_summary"])        # ← encripta

    new_patient = models.Patient(**data)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return desencriptar_paciente(new_patient)  # ← desencripta antes de devolver

@router.get("/", response_model=List[schemas.PatientResponse])
def get_patients(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico", "paciente"))
):
    patients = db.query(models.Patient).offset(offset).limit(limit).all()
    return [desencriptar_paciente(p) for p in patients]

@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico", "paciente"))
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return desencriptar_paciente(patient)

@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: str,
    updated: schemas.PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico"))
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    data = updated.dict()
    data["identification_doc"] = encrypt(data["identification_doc"])
    data["medical_summary"] = encrypt(data["medical_summary"])

    for key, value in data.items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return desencriptar_paciente(patient)

@router.patch("/{patient_id}", response_model=schemas.PatientResponse)
def patch_patient(
    patient_id: str,
    updates: schemas.PatientUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico"))
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    data = updates.dict(exclude_unset=True)
    if "identification_doc" in data:
        data["identification_doc"] = encrypt(data["identification_doc"])
    if "medical_summary" in data:
        data["medical_summary"] = encrypt(data["medical_summary"])

    for key, value in data.items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return desencriptar_paciente(patient)

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.delete(patient)
    db.commit()
    return {"message": "Paciente eliminado correctamente"}