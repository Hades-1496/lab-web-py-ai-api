from pydantic import BaseModel
from typing import Optional

class NotaEntrada(BaseModel):
    titulo: str
    contenido: str

class NotaSalida(BaseModel):
    id: int
    usuario_id: int
    titulo: str
    contenido: str