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
DATABASE_URL=postgresql://usuario:contraseña@host/nombre_db
ACCESS_KEY=TU_ACCESS_KEY_AQUI
ENCRYPT_KEY=TU_CLAVE_FERNET_AQUI

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
- **X-Access-Key**: llave global del sistema
- **X-Permission-Key**: llave del usuario con su rol

| Rol | Permisos |
|-----|---------|
| Admin | CRUD completo + gestión de usuarios |
| Médico | Crear y editar pacientes y observaciones |
| Paciente | Solo lectura |

> Las API Keys se configuran en las variables de entorno del servidor
> y se asignan a cada usuario al momento de su creación en la base de datos.




