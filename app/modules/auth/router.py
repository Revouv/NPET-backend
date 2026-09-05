"""
Rotas REST de Autenticação (camada Controller)

Só cuida de HTTP: recebe o DTO já validado pelo schema, chama o Service e devolve a resposta.
"""

from fastapi import APIRouter, Depends

from app.modules.auth.repository import AuthRepository, get_auth_repository
from app.modules.auth.schemas import LoginRequest, LoginResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_service(
    repository: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(repository)


@router.post("/login", response_model=LoginResponse, summary="Autentica com e-mail e senha")
def login(payload: LoginRequest, service: AuthService = Depends(get_service)):
    message = service.login(payload.email, payload.password)
    return LoginResponse(success=True, message=message)
