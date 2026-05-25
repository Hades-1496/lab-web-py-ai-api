# routes/notas.py
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from models.nota import NotaEntrada, NotaSalida
from services.service import NotaService
from auth.depend import obtener_db, verificar_token

router = APIRouter(prefix="/notas", tags=["Notas"])

@router.get("/", response_model=List[NotaSalida])
def listar_o_buscar(
    buscar: Optional[str] = None,
    db: dict = Depends(obtener_db),
    usuario: dict = Depends(verificar_token)
):
    return NotaService.listar_y_filtrar(usuario["usuario_id"], buscar, db)

@router.get("/{id}", response_model=NotaSalida)
def id_notas(id: int, db: dict = Depends(obtener_db), usuario: dict = Depends(verificar_token)):
    return NotaService.obtener_nota(id, usuario["usuario_id"], db)

@router.post("/", response_model=NotaSalida, status_code=status.HTTP_201_CREATED)
def crear_nota(
    nota: NotaEntrada,
    db: dict = Depends(obtener_db),
    usuario: dict = Depends(verificar_token)
):
    return NotaService.crear_nota(nota, usuario["usuario_id"], db)

@router.put("/{id}", response_model=NotaSalida)
def editar_nota(
    id: int, 
    nota_editada: NotaEntrada, 
    db: dict = Depends(obtener_db), 
    usuario: dict = Depends(verificar_token)
):
    return NotaService.editar_nota(id, usuario["usuario_id"], nota_editada, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_nota(id: int, db: dict = Depends(obtener_db), usuario: dict = Depends(verificar_token)):
    NotaService.eliminar_nota(id, usuario["usuario_id"], db)
    # Al usar 204_NO_CONTENT, no se debe devolver contenido
    return