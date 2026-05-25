# db/db.py

# Almacena los usuarios registrados
# Formato: {"id": 1, "email": "user@example.com", "hashed_password": "..."}
db_usuarios = []

# Almacena las notas
# Formato: {"id": 1, "usuario_id": 1, "titulo": "Ideas", "contenido": "..."}
db_notas = []

# Almacena las sesiones y el historial de chat de la IA
# Usar un diccionario con el 'session_id' como clave permite búsquedas rápidas.
# Ejemplo de estructura:
# {
#     "sesion-123": {
#         "usuario_id": 1,
#         "mensajes": [
#             {"rol": "usuario", "contenido": "Hola"}, 
#             {"rol": "ia", "contenido": "¡Hola! ¿En qué te ayudo?"}
#         ]
#     }
# }
db_sesiones_ia = {}
