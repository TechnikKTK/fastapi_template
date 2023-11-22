from pydantic import Field
from pydantic_settings import BaseSettings


class BaseDbConfig(BaseSettings):
    DB_TYPE: str

    @property
    def db_url(self):
        raise NotImplementedError


class PostgresConfig(BaseDbConfig):
    PG_USER: str
    PG_PASSWORD: str
    PG_NAME: str
    PG_HOST: str = Field(default="localhost")
    DB_TYPE: str = Field(default="postgresql")
    PG_PORT: int = Field(default=5432)

    @property
    def db_url(self):
        return (
            f"{self.DB_TYPE}://{self.PG_USER}:{self.PG_PASSWORD}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"
        )

    @property
    def db_async_url(self):
        return self.db_url.replace("://", "+asyncpg://", 1)


class RedisConfig(BaseDbConfig):
    REDIS_DB: int = Field(default=1)
    DB_TYPE: str = Field(default="redis")
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)

    @property
    def db_url(self):
        return (
            f"{self.DB_TYPE}://{self.REDIS_HOST}:"
            f"{self.REDIS_PORT}/{self.REDIS_DB}"
        )
