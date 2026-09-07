from app.modules.institutions.fake_db import FAKE_INSTITUTION_CREDENTIALS_DB


class InstitutionAuthRepository:
    # [Auth Instituição, camada: Repository]
    def find_credential(self, email: str) -> dict[str, str] | None:
        return next(
            (c for c in FAKE_INSTITUTION_CREDENTIALS_DB if c["email"] == email), None
        )


# Instância única usada pela injeção de dependência do FastAPI.
_repository = InstitutionAuthRepository()


def get_institution_auth_repository() -> InstitutionAuthRepository:
    return _repository
