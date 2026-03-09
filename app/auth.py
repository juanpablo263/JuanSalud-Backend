from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import os

VALID_ACCESS_KEY = os.getenv("ACCESS_KEY", "GLOBAL123")

def verify_access_key(x_access_key: str = Header(...)):
    if x_access_key != VALID_ACCESS_KEY:
        raise HTTPException(status_code=401, detail="Access key inválida")

def get_current_user(
    x_permission_key: str = Header(...),
    db: Session = Depends(get_db)
) -> models.User:
    user = db.query(models.User).filter(
        models.User.permission_key == x_permission_key
    ).first()
    if not user:
        raise HTTPException(status_code=403, detail="Permission key inválida")
    return user

def require_role(*roles: str):
    def checker(user: models.User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Sin permisos para esta acción")
        return user
    return checker