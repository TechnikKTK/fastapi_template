from pydantic import Field
from pydantic_settings import BaseSettings

from . import db as db_conf


class ServerConfig(BaseSettings):
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    LOGLEVEL: str = Field(default="DEBUG")


class Config(BaseSettings):
    server: ServerConfig
    main_db: db_conf.PostgresConfig
    cache_db: db_conf.RedisConfig
    APP_NAME: str
