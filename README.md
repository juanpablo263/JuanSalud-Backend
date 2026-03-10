# JuanSalud - Backend API REST FHIR

API REST desarrollada con FastAPI y PostgreSQL para gestión de historias clínicas.

## Tecnologías
- Python 3.11
- FastAPI
- PostgreSQL (Render)
- SQLAlchemy
- Cryptography (Fernet)
- SlowAPI (Rate Limiting)

## Instalación local

1. Clonar el repositorio:
git clone https://github.com/tu-usuario/JuanSalud-Backend.git
cd JuanSalud-Backend

2. Crear entorno virtual:
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias:
pip install -r requirements.txt

4. Crear archivo .env:
DATABASE_URL=postgresql://juanpablosalud_db_user:lFvQNoPZdsvyrK5ATqOv38oupquKjtcA@dpg-d6j1n6h5pdvs73aebes0-a.oregon-postgres.render.com/juanpablosalud_db
ACCESS_KEY=GLOBAL123
ENCRYPT_KEY=fNzItSYFiviHjk3TG9G9l_Hu8W3PVEQdf9U4TK34Xys=

5. Levantar el servidor:
uvicorn app.main:app --reload

## Endpoints principales
- POST /JuanSalud/Patient/ — Crear paciente
- GET /JuanSalud/Patient/ — Listar pacientes (paginado)
- POST /JuanSalud/Observation/ — Crear observación
- GET /JuanSalud/Observation/ — Listar observaciones
- POST /JuanSalud/users/ — Crear usuario (solo admin)

## Seguridad
Todos los endpoints requieren doble API Key en los headers:
- X-Access-Key: llave global del sistema (GLOBAL123)
- X-Permission-Key: llave del usuario con su rol (Para entrar como médico: Permission Key: a4add66322f6ed5f8be545fce465bff8bde7ff80d8c00189, Para entrar como paciente: Permission Key: 7304affb3136ef012ff34f6a0a0bae0f97ab0c2a21b2b31d, Para entrar como admin: Permission Key: ADMIN123)







