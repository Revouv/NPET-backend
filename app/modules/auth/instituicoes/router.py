from fastapi import APIRouter, Depends

from app.modules.auth.instituicoes.repository import (
    InstitutionAuthRepository,
    get_institution_auth_repository,
)
from app.modules.auth.instituicoes.schemas import (
    InstitutionLoginRequest,
    InstitutionLoginResponse,
)
from app.modules.auth.instituicoes.service import InstitutionAuthService

router = APIRouter(prefix="/institutions/auth", tags=["institutions-auth"])


def get_service(
    repository: InstitutionAuthRepository = Depends(get_institution_auth_repository),
) -> InstitutionAuthService:
    return InstitutionAuthService(repository)


@router.post(
    "/login",
    response_model=InstitutionLoginResponse,
    summary="Autentica uma instituição com e-mail e senha",
)
def login(
    payload: InstitutionLoginRequest,
    service: InstitutionAuthService = Depends(get_service),
):
    # [Auth Instituição, camada: Router]
    message = service.login(payload.email, payload.password)
    return InstitutionLoginResponse(success=True, message=message)
