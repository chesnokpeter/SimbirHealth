from typing import Any, Generic, Type, TypeAlias, TypeVar

from core.models.abstract import (
    AbsModel,
    DbAbsModel,
)

AbsSession: TypeAlias = Any

TSESSION = TypeVar('TSESSION', bound=AbsSession)


class AbsRepo(Generic[TSESSION]):
    model: AbsModel
    reponame: str

    def __init__(self, require_connector: str):
        self.require_connector = require_connector

    def __call__(self, session: TSESSION) -> AbsModel:
        self.session = session


class DbAbsRepo(AbsRepo[TSESSION]):
    model: DbAbsModel

    async def get(self):
        raise NotImplementedError

    async def get_one(self):
        raise NotImplementedError

    async def add(self):
        raise NotImplementedError

    async def offset(self):
        raise NotImplementedError

    async def update(self):
        raise NotImplementedError

    async def delete(self):
        raise NotImplementedError
