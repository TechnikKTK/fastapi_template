from app.apps import register_app_routes
from app.config import App, load_config
from app.settings.server import Config, Misc


def make_app() -> App:
    misc = Misc()
    app_config = load_config(
        misc.TOML_CONFIG, misc.PSQL_ENV, misc.REDIS_ENV, misc.MAIN_ENV, misc
    )
    app = App(app_config)
    register_app_routes(app)
    return app
