# auth/jwt.py

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException
import os

SECRET_KEY = os.getenv("SECRET_KEY", "cambiadito")
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def crear_token(datos: dict) -> str:
    payload = datos.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")