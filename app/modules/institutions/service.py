from app.core.exceptions import UnauthorizedError
from app.modules.institutions.repository import InstitutionAuthRepository


class InstitutionAuthService:
    def __init__(self, repository: InstitutionAuthRepository) -> None:
        self._repository = repository

    def login(self, email: str, password: str) -> str:
        # [Auth Instituição, camada: Service]
        credential = self._repository.find_credential(email)
        if credential is None or credential["password"] != password:
            raise UnauthorizedError("E-mail ou senha inválidos.")
        return "Autenticação realizada com sucesso."
