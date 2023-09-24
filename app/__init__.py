from app.apps import register_app_routes
from app.config import App, APP_CONFIG

app = App(APP_CONFIG)
register_app_routes(app)
