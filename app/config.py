import tomllib
from pathlib import Path

from fastapi import FastAPI

from app.settings.db import PostgresConfig, RedisConfig
from app.settings.server import Config, ServerConfig

BASE_DIR = Path(__file__).parent.parent
APP_DIR = BASE_DIR / 'app'
MAIN_ENV = APP_DIR / '.envs/.env'
PSQL_ENV = APP_DIR / '.envs/psql.env'
REDIS_ENV = APP_DIR / '.envs/redis.env'
TOML_CONFIG = APP_DIR / 'config.toml'


class App(FastAPI):

    def __init__(self, config: Config):
        super().__init__(
            title=config.APP_NAME,
            debug=config.server.DEBUG
        )
        self.config = config


def load_config(
    config_toml_path: str | Path,
    psql_env_path: str | Path,
    redis_env_path: str | Path,
    others_env_path: str | Path,
) -> Config:
    with open(config_toml_path, 'rb') as file:
        config = tomllib.load(file)
    server_config = ServerConfig(**config['server'])
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
        main_db=pg_db_config,
        cache_db=redis_conf,
        **config['app']
    )


APP_CONFIG = load_config(TOML_CONFIG, PSQL_ENV, REDIS_ENV, MAIN_ENV)
