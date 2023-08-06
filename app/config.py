import tomllib
from pathlib import Path
from typing import Type

import app.settings.db as db_conf
from app.settings.server import Config, ServerConfig


def load_config(
    config_toml_path: str | Path,
    db_env_path: str | Path,
    others_env_path: str | Path,
    main_db_conf_class: Type[db_conf.BaseDbConfig]
) -> Config:
    with open(config_toml_path, 'rb') as file:
        config = tomllib.load(file)
    server_config = ServerConfig(**config['server'])
    db_config = main_db_conf_class(
        _env_file=db_env_path,
        _case_sensitive=False
    )
    return Config(
        _env_file=others_env_path,
        _case_sensitive=False,
        server=server_config,
        main_db=db_config,
        **config['app']
    )
