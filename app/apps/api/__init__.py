from fastapi import APIRouter

from app.apps.api.v1 import register_v1_api_routes


def register_api_routes() -> APIRouter:
    api_router = APIRouter(prefix="/api")
    api_router.include_router(register_v1_api_routes())
    return api_router
