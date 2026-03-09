import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models
from app.database import get_db
from app.auth import verify_access_key, require_role

router = APIRouter(
    prefix="/JuanSalud/users",
    tags=["Users"],
    dependencies=[Depends(verify_access_key)]
)

class UserCreate(BaseModel):
    username: str
    role: str  # admin, medico, paciente

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    permission_key: str

    class Config:
        from_attributes = True

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    if data.role not in ["admin", "medico", "paciente"]:
        raise HTTPException(status_code=400, detail="Rol inválido. Usa: admin, medico, paciente")

    existing = db.query(models.User).filter(models.User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = models.User(
        username=data.username,
        role=data.role,
        access_key=secrets.token_hex(16),
        permission_key=secrets.token_hex(24)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return db.query(models.User).all()

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    target = db.query(models.User).filter(models.User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(target)
    db.commit()

    # TEMPORAL - Eliminar después de crear el primer admin
@router.post("/setup", response_model=UserResponse, status_code=201)
def create_first_admin(data: UserCreate, db: Session = Depends(get_db)):
    if data.role != "admin":
        raise HTTPException(status_code=400, detail="Solo puedes crear admin por esta ruta")
    
    existing = db.query(models.User).filter(models.User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = models.User(
        username=data.username,
        role="admin",
        access_key=secrets.token_hex(16),
        permission_key=secrets.token_hex(24)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user