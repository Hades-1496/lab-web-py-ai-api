from fastapi import FastAPI, Request
from routes.auth import router as auth_router
from routes.notas import router as notas_router
from routes.ia import router as ia_router
from errors.errorHandler import register_error_handlers
import uvicorn
import os
import json
import time

app = FastAPI(title="API IA-ready con Autenticación", version="1.0.0")

# Registramos los manejadores de errores
register_error_handlers(app)

# Incluimos los routers
app.include_router(auth_router)
app.include_router(notas_router)
app.include_router(ia_router)

@app.middleware("http")
async def json_logger_middleware(request: Request, call_next):
    # Verificamos si la ruta es de la API de IA
    if request.url.path.startswith("/api/"):
        start_time = time.time()
        response = await call_next(request)
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        
        log_info = {
            "level": "INFO",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time_ms": process_time_ms
        }
        print(json.dumps(log_info))
        return response
    else:
        return await call_next(request)

@app.get("/")
def ruta_raiz():
    return {"mensaje": "Bienvenido a la API de Notas lista para Agentes de IA"}


# Nunca me acuerdo de usar "uvicorn main:app --reload", así que hago esto para ejecutarl con "python main.py"
if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=True)