# auth/depend.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import decodificar_token
from db.db import db_usuarios, db_notas, db_sesiones_ia

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Sistema de dependencias

def obtener_db():
    """Simula una conexión a base de datos"""
    db = {
        "usuarios": db_usuarios,
        "notas": db_notas,
        "sesiones_ia": db_sesiones_ia
    }
    try:
        yield db
    finally:
        pass

def verificar_token(token: str = Depends(oauth2_scheme)):
    # decodificar_token ya lanza una excepción (HTTPException 401) si es inválido
    datos_usuario = decodificar_token(token)
    return datos_usuario
