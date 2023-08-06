from pathlib import Path

from fastapi import FastAPI

from app.config import load_config
from app.settings.server import Config
import app.settings.db as db_conf


class MateGPT(FastAPI):

    def __init__(self, app_config: Config, **kwargs):
        super().__init__(title=app_config.APP_NAME, **kwargs)
        self.app_config = app_config
        self.debug = self.app_config.server.DEBUG


def make_app() -> MateGPT:
    base_dir = Path(__file__).parent
    main_env = base_dir / '.envs/.env'
    config_toml_path = base_dir / 'config.toml'
    db_env = base_dir / '.envs/db.env'
    app_config = load_config(
        config_toml_path,
        db_env, main_env,
        db_conf.PostgresConfig
    )
    return MateGPT(
        app_config
    )
