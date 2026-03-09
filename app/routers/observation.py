import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth import verify_access_key, require_role
from app.limiter import limiter

router = APIRouter(
    prefix="/JuanSalud/Observation",
    tags=["Observation"],
    dependencies=[Depends(verify_access_key)]
)

@router.post("/", response_model=schemas.ObservationResponse, status_code=201)
@limiter.limit("20/minute")
def create_observation(
    request: Request,
    data: schemas.ObservationCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico"))
):
    patient = db.query(models.Patient).filter(models.Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    obs = models.Observation(id=str(uuid.uuid4()), **data.model_dump())
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

@router.get("/", response_model=list[schemas.ObservationResponse])
def list_observations(
    patient_id: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico", "paciente"))
):
    query = db.query(models.Observation)
    if patient_id:
        query = query.filter(models.Observation.patient_id == patient_id)
    return query.offset(offset).limit(limit).all()

@router.get("/{obs_id}", response_model=schemas.ObservationResponse)
def get_observation(
    obs_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico", "paciente"))
):
    obs = db.query(models.Observation).filter(models.Observation.id == obs_id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observación no encontrada")
    return obs

@router.put("/{obs_id}", response_model=schemas.ObservationResponse)
def update_observation(
    obs_id: str,
    data: schemas.ObservationCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "medico"))
):
    obs = db.query(models.Observation).filter(models.Observation.id == obs_id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observación no encontrada")
    for key, value in data.model_dump().items():
        setattr(obs, key, value)
    db.commit()
    db.refresh(obs)
    return obs

@router.delete("/{obs_id}", status_code=204)
def delete_observation(
    obs_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    obs = db.query(models.Observation).filter(models.Observation.id == obs_id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observación no encontrada")
    db.delete(obs)
    db.commit()