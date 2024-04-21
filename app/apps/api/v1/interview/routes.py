from fastapi import APIRouter

from app.apps.schemas import ApiResponseStatus
from app.config import App

from . import views


def register_interview_routes(app: App) -> APIRouter:
    api_router = APIRouter(prefix="/interview")
    api_router.add_api_route(
        "/tasks",
        endpoint=views.interview_task_create,
        name=app.config.url_names.INTERVIEW_TASK_CREATE,
        methods=["POST"],
        response_model=ApiResponseStatus,
    )
    return api_router
