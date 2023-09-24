from fastapi import APIRouter

from . import views


def register_core_routes() -> APIRouter:
    api_router = APIRouter(prefix="/core")
    api_router.add_api_route("/", endpoint=views.core, name="core_get")
    return api_router
