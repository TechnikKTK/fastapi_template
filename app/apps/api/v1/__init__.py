from fastapi import APIRouter

from app.apps.api.v1.core.routes import register_core_routes


def register_v1_api_routes() -> APIRouter:
    api_router = APIRouter(prefix='/v1')
    api_router.include_router(register_core_routes())
    return api_router
