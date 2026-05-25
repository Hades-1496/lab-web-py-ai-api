from pydantic import BaseModel, EmailStr, Field

class UsuarioRegistro(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str