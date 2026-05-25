from auth.jwt import hashear_password, verificar_password, crear_token
from fastapi import HTTPException, status

class UsuarioService:
    @staticmethod
    def registrar(datos: dict, db: dict):
        # Verificar si el email ya existe
        for u in db["usuarios"]:
            if u["email"] == datos.email:
                raise HTTPException(status_code=400, detail="El email ya está registrado")
        
        nuevo_usuario = {
            "id": len(db["usuarios"]) + 1,
            "email": datos.email,
            "hashed_password": hashear_password(datos.password)
        }
        db["usuarios"].append(nuevo_usuario)
        return {"id": nuevo_usuario["id"], "email": nuevo_usuario["email"]}

    @staticmethod
    def login(datos: dict, db: dict):
        usuario_encontrado = None
        for u in db["usuarios"]:
            if u["email"] == datos.email:
                usuario_encontrado = u
                break
        
        if not usuario_encontrado or not verificar_password(datos.password, usuario_encontrado["hashed_password"]):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        # Creamos el token guardando el ID del usuario dentro de él
        token = crear_token({"usuario_id": usuario_encontrado["id"], "email": usuario_encontrado["email"]})
        return {"access_token": token, "token_type": "bearer"}
    
class NotaService:
    @staticmethod
    def crear_nota(datos: dict, usuario_id: int, db: dict):
        nueva_nota = {
            "id": len(db["notas"]) + 1,
            "usuario_id": usuario_id,
            "titulo": datos.titulo,
            "contenido": datos.contenido
        }
        db["notas"].append(nueva_nota)
        return nueva_nota

    @staticmethod
    def listar_y_filtrar(usuario_id: int, buscar: str, db: dict):
        # 1. Filtramos para que el usuario solo vea SUS notas
        mis_notas = [n for n in db["notas"] if n["usuario_id"] == usuario_id]
        
        # 2. Si hay un parámetro de búsqueda, filtramos por título o contenido
        if buscar:
            buscar = buscar.lower()
            mis_notas = [n for n in mis_notas if buscar in n["titulo"].lower() or buscar in n["contenido"].lower()]
        
        return mis_notas

    @staticmethod
    def obtener_nota(id: int, usuario_id: int, db: dict):
        nota = next((n for n in db["notas"] if n["id"] == id and n["usuario_id"] == usuario_id), None)
        if not nota:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        return nota

    @staticmethod
    def editar_nota(id: int, usuario_id: int, datos: dict, db: dict):
        nota = NotaService.obtener_nota(id, usuario_id, db)
        nota["titulo"] = datos.titulo
        nota["contenido"] = datos.contenido
        return nota

    @staticmethod
    def eliminar_nota(id: int, usuario_id: int, db: dict):
        nota = NotaService.obtener_nota(id, usuario_id, db)
        db["notas"].remove(nota)
        return {"mensaje": "Nota eliminada con éxito"}
    
class IAService:
    @staticmethod
    def simular_chat(session_id: str, mensaje_usuario: str, usuario_id: int, db: dict):
        # Si la sesión no existe en el diccionario, la inicializamos
        if session_id not in db["sesiones_ia"]:
            db["sesiones_ia"][session_id] = {
                "usuario_id": usuario_id,
                "mensajes": []
            }
        
        historial = db["sesiones_ia"][session_id]["mensajes"]
        historial.append({"rol": "usuario", "contenido": mensaje_usuario})
        
        # Simulación de respuesta de IA basada en contexto básico
        respuesta_ia = f"¡Hola! He recibido tu mensaje: '{mensaje_usuario}'. Como agente de IA, estoy listo para analizar tus notas asignadas al usuario {usuario_id}."
        historial.append({"rol": "ia", "contenido": respuesta_ia})
        
        return {"respuesta": respuesta_ia, "session_id": session_id, "historial": historial}

    @staticmethod
    def resumir_nota(nota_id: int, usuario_id: int, db: dict):
        nota = NotaService.obtener_nota(nota_id, usuario_id, db)
        # Simulación de respuesta de resumen
        resumen = f"Simulación de IA: La nota trata sobre '{nota['titulo']}'. Puntos clave detectados: {nota['contenido'][:40]}..."
        return {"nota_id": nota_id, "resumen_ia": resumen}
    
