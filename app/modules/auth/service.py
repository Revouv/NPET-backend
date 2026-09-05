"""
Regras de negócio de Autenticação (camada Service)

Não conhece HTTP nem sabe onde os dados estão guardados: pede ao Repository a credencial e decide se a autenticação é válida.
"""

from app.core.exceptions import UnauthorizedError
from app.modules.auth.repository import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self._repository = repository

    def login(self, email: str, password: str) -> str:
        credential = self._repository.find_credential(email)
        if credential is None or credential["password"] != password:
            raise UnauthorizedError("E-mail ou senha inválidos.")
        return "Autenticação realizada com sucesso."
