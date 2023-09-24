from fastapi import FastAPI

from app.apps.api import register_api_routes


def register_app_routes(app: FastAPI):
    app.include_router(register_api_routes())
