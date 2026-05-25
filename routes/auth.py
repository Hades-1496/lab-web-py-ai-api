# routes/auth.py
from fastapi import APIRouter, Depends, status
from models.usuario import UsuarioRegistro, UsuarioLogin, TokenResponse
from services.service import UsuarioService
from auth.depend import obtener_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar(datos: UsuarioRegistro, db: dict = Depends(obtener_db)):
    # Delegamos al servicio pasando los datos y la base de datos inyectada
    return UsuarioService.registrar(datos, db)

@router.post("/login", response_model=TokenResponse)
def login(datos: UsuarioLogin, db: dict = Depends(obtener_db)):
    return UsuarioService.login(datos, db)