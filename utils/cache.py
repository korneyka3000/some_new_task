from contextlib import asynccontextmanager
from typing import AsyncIterator

from redis.asyncio import Redis

from utils.config import CacheSettings


class Cache:
    def __init__(
            self,
            settings: CacheSettings
    ) -> None:
        self.settings = settings
        self.engine = None
        self.url = None
        self.ctx_conn = asynccontextmanager(self.get_conn)

    def configure(self) -> None:
        self.url = 'redis://' \
                   f'{self.settings.REDIS_HOST}:' \
                   f'{self.settings.REDIS_PORT}/' \
                   f'{self.settings.REDIS_DB}' \
                   '?decode_responses=True'
        self.engine = Redis.from_url(self.url)

    async def get_conn(self) -> AsyncIterator[Redis]:
        if not self.engine:
            self.configure()

        async with self.engine.client() as conn:
            yield conn


redis_client = Cache(CacheSettings(_env_file='.env'))


async def conn_cache():
    async with redis_client.ctx_conn() as conn:
        yield conn
