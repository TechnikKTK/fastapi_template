from sqlalchemy import create_engine
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.apps import register_app_routes
from app.config import App, load_config
from app.db.postgres.db_async import AsyncPostgresEngine
from app.db.postgres.db_sync import SyncPgEngine
from app.settings.server import Config, Misc


def make_app() -> App:
    misc = Misc()
    app_config = load_config(
        misc.TOML_CONFIG, misc.PSQL_ENV, misc.REDIS_ENV, misc.MAIN_ENV, misc
    )
    main_db_async = AsyncPostgresEngine(app_config.main_db)
    main_db_sync = SyncPgEngine(create_engine(app_config.main_db.db_url))
    app = App(app_config, main_db_async, main_db_sync)
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=app.config.app.ALLOWED_HOSTS
    )
    register_app_routes(app)
    return app
