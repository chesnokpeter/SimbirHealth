from typing import Callable

import asyncio_redis
from asyncio_redis import RedisProtocol

from core.infra.abstract import AbsConnector


def get_async_conn_redis(redis_host: str, redis_port: int) -> Callable[[], RedisProtocol]:
    return lambda: asyncio_redis.Connection.create(host=redis_host, port=redis_port)


class RedisConnector(AbsConnector):
    def __init__(self, redis_host: str, redis_port: int, connector_name: str = 'redis'):
        self.maker = get_async_conn_redis(redis_host, redis_port)
        self.connector_name = connector_name

    async def connect(self):
        self._session = await self.maker()

    async def commit(self): ...
    async def rollback(self): ...
    async def close(self):
        self._session.close()

    @property
    def session(self):
        return self._session
