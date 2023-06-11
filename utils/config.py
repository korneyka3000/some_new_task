from pydantic import BaseSettings


class CacheSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int = 0
