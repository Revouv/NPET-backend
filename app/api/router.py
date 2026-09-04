"""Roteador principal da API.

Agrega os routers de todos os módulos/domínios. É incluído em `app.main`
sob o prefixo definido em `settings.API_PREFIX` (ex.: `/api/v1`).
"""

from fastapi import APIRouter

from app.health.router import router as health_router

api_router = APIRouter()

api_router.include_router(health_router)
