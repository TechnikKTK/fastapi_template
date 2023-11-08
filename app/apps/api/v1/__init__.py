from fastapi import APIRouter

from app.apps.api.v1.core.routes import register_core_routes
from app.config import App


def register_v1_api_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/v1")
    api_router.include_router(register_core_routes(app))
    return api_router
