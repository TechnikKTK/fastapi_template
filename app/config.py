import tomllib
from pathlib import Path

from fastapi import FastAPI

from app.db.postgres.db_async import AsyncPostgresEngine
from app.db.postgres.db_sync import SyncPgEngine
from app.settings.db import PostgresConfig, RedisConfig
from app.settings.server import AppConfig, Config, Misc, ServerConfig


class App(FastAPI):
    def __init__(
        self,
        config: Config,
        async_pg_engine: AsyncPostgresEngine,
        sync_pg_engine: SyncPgEngine,
    ):
        super().__init__(title=config.app.APP_NAME, debug=config.server.DEBUG)
        self.config = config
        self.db_async = async_pg_engine
        self.db_sync = sync_pg_engine


def load_config(
    config_toml_path: str | Path,
    psql_env_path: str | Path,
    redis_env_path: str | Path,
    others_env_path: str | Path,
    misc: Misc | None = None,
) -> Config:
    with open(config_toml_path, "rb") as file:
        config = tomllib.load(file)
    if not misc:
        misc = Misc()
    server_config = ServerConfig(**config["server"])
    app_config = AppConfig(**config["app"])
    pg_db_config = PostgresConfig(
        _env_file=psql_env_path,  # type: ignore
        _case_sensitive=False,  # type: ignore
    )
    redis_conf = RedisConfig(
        _env_file=redis_env_path,  # type: ignore
        _case_sensitive=False,  # type: ignore
    )
    return Config(
        _env_file=others_env_path,  # type: ignore
        _case_sensitive=False,  # type: ignore
        server=server_config,
        app=app_config,
        main_db=pg_db_config,
        cache_db=redis_conf,
        misc=misc,
    )
