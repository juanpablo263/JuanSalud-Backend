from cryptography.fernet import Fernet
import os

KEY = os.getenv("ENCRYPT_KEY")
if not KEY:
    raise RuntimeError("ENCRYPT_KEY no está definida en el .env")

fernet = Fernet(KEY.encode())

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(text: str) -> str:
    return fernet.decrypt(text.encode()).decode()