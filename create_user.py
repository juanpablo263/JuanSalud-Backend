from app.database import SessionLocal
from app.models import User

db = SessionLocal()

user1 = User(
    id="1",
    username="admin1",
    role="admin",
    access_key="GLOBAL123",
    permission_key="ADMIN123"
)

db.add(user1)
db.commit()
db.close()