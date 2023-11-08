from app.apps.api import register_api_routes
from app.config import App


def register_app_routes(app: App):
    app.include_router(register_api_routes(app))
