import json
from typing import Generic, Type, TypeVar

from asyncio_redis import RedisProtocol

from core.repos.abstract import MemoryAbsRepo, MemoryAbsModel


T = TypeVar('T', bound=MemoryAbsModel)


class RedisDefaultRepo(Generic[T], MemoryAbsRepo[RedisProtocol]):
    model: Type[T]

    def __init__(self, require_connector: str = 'redis'):
        self.require_connector = require_connector

    async def get(self, key: str) -> T | None:
        data = await self.session.get(key)  # type: ignore
        if not data:
            return None
        data = json.loads(data)
        memory_model_name = data.pop('memory_model_name', None)
        if memory_model_name != self.model.__name__:
            return None
        return self.model(**data)

    async def add(self, key: str, data: T) -> None:
        await self.session.set(key, json.dumps(data.model_dump()))  # type: ignore

    async def delete(self, key: str) -> None:
        await self.session.delete(keys=[key])  # type: ignore
