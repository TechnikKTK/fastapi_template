from typing import Any

import sqlalchemy as sa
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio.exc import AsyncMethodRequired

from app.settings.db import PostgresConfig
from app.utils.patterns.singleton import SingletonMeta


class AsyncPostgresEngine(AsyncEngine, metaclass=SingletonMeta):

    def __init__(self, pg_config: PostgresConfig, **params):
        self.pg_config = pg_config
        super().__init__(self._init_sync_engine(pg_config, **params))
        self.session_class = async_sessionmaker(self)

    def _init_sync_engine(self, config: PostgresConfig, **kwargs) -> sa.Engine:
        if kwargs.get("server_side_cursors", False):
            raise AsyncMethodRequired(
                "Can't set server_side_cursors for async engine globally; "
                "use the connection.stream() method for an async "
                "streaming result set"
            )
        kwargs["_is_async"] = True
        async_creator = kwargs.pop("async_creator", None)
        if async_creator:
            if kwargs.get("creator", None):
                raise ArgumentError(
                    "Can only specify one of 'async_creator' or 'creator', "
                    "not both."
                )

            def creator() -> Any:
                return sync_engine.dialect.dbapi.connect(  # type: ignore
                    async_creator_fn=async_creator
                )
            kwargs["creator"] = creator
        sync_engine = sa.create_engine(config.db_async_url, **kwargs)
        return sync_engine
