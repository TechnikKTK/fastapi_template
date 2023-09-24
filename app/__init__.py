from app.apps import register_app_routes
from app.config import APP_CONFIG, App


app = App(APP_CONFIG)
register_app_routes(app)
