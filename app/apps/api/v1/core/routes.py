from fastapi import APIRouter

from app.config import App

from . import views


def register_core_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/core")
    api_router.add_api_route(
        "/", endpoint=views.core, name=app.config.CORE_GET
    )
    return api_router
