from fastapi import APIRouter

from app.config import App

from . import views
from .schemas import DsTaskCreatedResponse


def register_ds_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/core")
    api_router.add_api_route(
        "/tasks",
        endpoint=views.ds_task_create,
        name=app.config.url_names.DS_TASK_CREATE,
        methods=["POST"],
        response_model=DsTaskCreatedResponse,
    )
    return api_router
