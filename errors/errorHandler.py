# errors/errorHandler.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
 
def register_error_handlers(app: FastAPI):
    # Error de validación Pydantic → respuesta legible
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errores = []
        for error in exc.errors():
            errores.append({
                "campo": " → ".join(str(loc) for loc in error["loc"]),
                "mensaje": error["msg"],
                "tipo": error["type"]
            })
        return JSONResponse(
            status_code=422,
            content={"ok": False, "error": "Datos inválidos", "detalles": errores}
        )
     
    # Error 404 personalizado
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={"ok": False, "error": f"Ruta {request.url.path} no encontrada"}
        )
     
    # Capturar errores no controlados
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": "Error interno del servidor"}
        )