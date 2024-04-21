from fastapi import APIRouter

from app.apps.api.v1.ds.routes import register_ds_routes
from app.apps.api.v1.interview.routes import register_interview_routes
from app.config import App


def register_v1_api_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/v1")
    api_router.include_router(register_ds_routes(app))
    api_router.include_router(register_interview_routes(app))
    return api_router
