from pydantic import Field
from pydantic_settings import BaseSettings


class BaseDbConfig(BaseSettings):
    DB_TYPE: str
    HOST: str = Field(default='localhost')
    PORT: int

    @property
    def db_url(self):
        raise NotImplementedError


class PostgresConfig(BaseDbConfig):
    USER: str
    PASSWORD: str
    DB_NAME: str

    @property
    def db_url(self):
        return (
            f"{self.DB_TYPE}://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.DB_NAME}"
        )


class RedisConfig(BaseDbConfig):
    DB_NUM: int = Field(default=1)

    @property
    def db_url(self):
        return (
            f"{self.DB_TYPE}://{self.HOST}:{self.PORT}/{self.DB_NUM}"
        )
