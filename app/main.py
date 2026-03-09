from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
from app.database import engine
from sqlalchemy import text
from app.models import Base
from app.routers import patient, user, observation

app = FastAPI(title="JuanPablo_Salud Backend")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

app.include_router(patient.router)
app.include_router(user.router)
app.include_router(observation.router)
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "Conexión exitosa"}
    except Exception as e:
        return {"error": str(e)}