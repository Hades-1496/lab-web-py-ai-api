# routes/ia.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from services.service import IAService, NotaService
from auth.depend import obtener_db, verificar_token

router = APIRouter(prefix="/api", tags=["IA"])

class PeticionChat(BaseModel):
    session_id: str
    mensaje: str

@router.post("/chat")
def chat(
    peticion: PeticionChat,
    db: dict = Depends(obtener_db),
    usuario: dict = Depends(verificar_token)
):
    return IAService.simular_chat(peticion.session_id, peticion.mensaje, usuario["usuario_id"], db)

@router.get("/chat/history/{session_id}")
def sesion(session_id: str, db: dict = Depends(obtener_db), usuario: dict = Depends(verificar_token)):
    sesion_ia = db["sesiones_ia"].get(session_id)
    
    # Verificamos que la sesión exista y pertenezca al usuario autenticado
    if not sesion_ia or sesion_ia["usuario_id"] != usuario["usuario_id"]:
        raise HTTPException(status_code=404, detail="Sesión no encontrada o no autorizada")
    
    return {"historial": sesion_ia["mensajes"]}

@router.get("/search")
def busqueda(q: str, db: dict = Depends(obtener_db), usuario: dict = Depends(verificar_token)):
    # Reutilizamos el servicio de Notas para la búsqueda de la IA
    notas_encontradas = NotaService.listar_y_filtrar(usuario["usuario_id"], q, db)
    return {"resultados": notas_encontradas}

@router.get("/context")
def contexto(db: dict = Depends(obtener_db), usuario: dict = Depends(verificar_token)):
    notas_totales = len([n for n in db["notas"] if n["usuario_id"] == usuario["usuario_id"]])
    return {
        "capacidades": [
            "Creación, edición y eliminación de notas",
            "Búsqueda semántica por palabras clave",
            "Chat contextual recordatorio sobre tus notas"
        ],
        "total_notas_usuario": notas_totales
    }

@router.post("/resumir/{nota_id}")
def resumir_nota(nota_id: int, db: dict = Depends(obtener_db), usuario: dict = Depends(verificar_token)):
    return IAService.resumir_nota(nota_id, usuario["usuario_id"], db)