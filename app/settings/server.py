from dataclasses import dataclass
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from . import db as db_conf


class CeleryConfig(BaseSettings):
    app_name: str
    broker_url: str
    imports: list[str] = []
    broker_connection_retry_on_startup: bool = False


class ServerConfig(BaseSettings):
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    LOGLEVEL: str = Field(default="DEBUG")


class AppConfig(BaseSettings):
    APP_NAME: str = "VISA DS API"
    DS_RESULT_CALLBACK_URL: str = "https://getvisa.center/api/ds/setStatus"
    INTERVIEW_RESULT_CALLBACK_URL: str = "https://getvisa.center/api/interview/update"
    ALLOWED_HOSTS: list[str] = ['*']


@dataclass
class Misc:
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    APP_DIR: Path = BASE_DIR / "app"
    ENVS_DIR: Path = APP_DIR / ".envs/"
    MAIN_ENV: Path = ENVS_DIR / ".env"
    PSQL_ENV: Path = ENVS_DIR / "psql.env"
    REDIS_ENV: Path = ENVS_DIR / "redis.env"
    CELERY_ENV: Path = ENVS_DIR / "celery.env"
    TOML_CONFIG: Path = APP_DIR / "config.toml"
    MEDIA_DIR: Path = BASE_DIR / "media"
    PHOTOS_DIR: Path = MEDIA_DIR / "photos"
    USER_PHOTOS_DIR: Path = PHOTOS_DIR / "users"

    @property
    def create_dirs(self) -> list[Path]:
        return [self.USER_PHOTOS_DIR]


@dataclass
class UrlNames:
    DS_TASK_CREATE: str = "create_ds_task"
    INTERVIEW_TASK_CREATE: str = "create_interview_task"


class Config(BaseSettings):
    app: AppConfig
    server: ServerConfig
    main_db: db_conf.PostgresConfig
    cache_db: db_conf.RedisConfig
    misc: Misc
    RUCAPTCHA_API_KEY: str ="2d77ec701ee5c539ec02a43e8e6467f2"
    url_names: UrlNames = UrlNames()
