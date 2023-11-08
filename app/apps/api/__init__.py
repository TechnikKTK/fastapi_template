from fastapi import APIRouter

from app.apps.api.v1 import register_v1_api_routes
from app.config import App


def register_api_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/api")
    api_router.include_router(register_v1_api_routes(app))
    return api_router
