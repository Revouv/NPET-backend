"""
Repositório de Autenticação (camada Repository)

Consulta a "tabela" de credenciais. Hoje, a lista hardcoded em `fake_db.py`. É o único ponto do módulo que sabe onde/como os dados estão guardados.
"""

from app.modules.auth.fake_db import FAKE_CREDENTIALS_DB


class AuthRepository:
    def find_credential(self, email: str) -> dict[str, str] | None:
        return next((c for c in FAKE_CREDENTIALS_DB if c["email"] == email), None)


# Instância única usada pela injeção de dependência do FastAPI.
_repository = AuthRepository()


def get_auth_repository() -> AuthRepository:
    return _repository
