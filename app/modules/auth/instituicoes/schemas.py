from pydantic import BaseModel, EmailStr, Field


class InstitutionLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class InstitutionLoginResponse(BaseModel):
    success: bool
    message: str
