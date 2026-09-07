"""
DTOs (Schemas) da API de Autenticação

`LoginRequest` também faz a validação das credenciais de entrada (formato de e-mail e senha) antes de chegar ao Service.
"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    success: bool
    message: str
