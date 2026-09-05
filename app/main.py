"""
Ponto de entrada da aplicação FastAPI.

Execute com:  uvicorn app.main:app --reload
Documentação: http://localhost:8000/docs
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import AppError


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description=(
            "API REST da plataforma NPET"
        ),
    )

    # CORS liberado para o frontend (React). Restrinja em produção.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Converte exceções de domínio em respostas HTTP JSON padronizadas.
    @app.exception_handler(AppError)
    async def _handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    app.include_router(api_router, prefix=settings.API_PREFIX)

    @app.get("/", tags=["root"], summary="Informações básicas da API")
    def root() -> dict[str, str]:
        return {
            "name": settings.APP_NAME,
            "env": settings.APP_ENV,
            "docs": "/docs",
            "api": settings.API_PREFIX,
        }

    return app


app = create_app()
