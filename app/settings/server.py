from dataclasses import dataclass
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from . import db as db_conf


class ServerConfig(BaseSettings):
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    LOGLEVEL: str = Field(default="DEBUG")


@dataclass
class Misc:
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    APP_DIR: Path = BASE_DIR / "app"
    MAIN_ENV: Path = APP_DIR / ".envs/.env"
    PSQL_ENV: Path = APP_DIR / ".envs/psql.env"
    REDIS_ENV: Path = APP_DIR / ".envs/redis.env"
    TOML_CONFIG: Path = APP_DIR / "config.toml"


class Config(BaseSettings):
    server: ServerConfig
    main_db: db_conf.PostgresConfig
    cache_db: db_conf.RedisConfig
    misc: Misc
    APP_NAME: str

    # Url names
    CORE_GET: str = "core_get"
