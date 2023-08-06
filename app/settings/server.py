from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

import app.settings.db as db_conf


class ServerConfig(BaseSettings):
    HOST: str = Field(default='127.0.0.1')
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    LOGLEVEL: str = Field(default='DEBUG')


class Config(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    server: ServerConfig
    main_db: db_conf.BaseDbConfig
    APP_NAME: str
