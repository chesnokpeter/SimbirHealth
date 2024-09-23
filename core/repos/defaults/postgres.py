from typing import Generic, Type, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from core.infra.abstract import DbAbsTable
from core.repos.abstract import DbAbsRepo

T = TypeVar('T', bound=DbAbsTable)


class PostgresDefaultRepo(Generic[T], DbAbsRepo[Session]):
    def __init__(self, require_connector: str = 'postgres'):
        self.require_connector = require_connector

    model: Type[T]

    async def get(self, **data) -> list[T] | None:
        result = await self.session.execute(
            select(self.model).order_by(self.model.id.desc()).filter_by(**data)
        )  # type: ignore
        return [i[0] for i in result.all()]

    async def get_one(self, **data) -> T | None:
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.first()
        return res[0] if res else res

    async def add(self, **data) -> T:
        stmt = insert(self.model).values(**data)
        stmt = stmt.returning(self.model)
        return await self.session.scalar(stmt)  # type: ignore

    async def offset(
        self, offset: int = 0, limit: int | None = None, order=None, **data
    ) -> list[T] | None:
        stmt = select(self.model).offset(offset).limit(limit).order_by(order).filter_by(**data)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.all()
        return [i[0] for i in res]

    async def update(self, id: int, **data) -> T:
        query = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        return await self.session.scalar(query)  # type: ignore

    async def delete(self, id: int) -> None:
        stmt = delete(self.model).where(self.model.id == id)  # type: ignore
        await self.session.execute(stmt)  # type: ignore
