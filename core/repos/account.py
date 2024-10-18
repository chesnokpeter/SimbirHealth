from core.infra.postgresql.tables import ACCOUNT
from core.repos.defaults.postgres import PostgresDefaultRepo
from sqlalchemy import delete, insert, select, update


class AccountRepo(PostgresDefaultRepo[ACCOUNT]):
    model = ACCOUNT
    reponame = 'account'

    async def get(self, **data) -> list[ACCOUNT] | None:
        result = await self.session.execute(
            select(self.model).order_by(self.model.id.desc()).filter_by(**data, is_deleted=False)
        )  # type: ignore
        return [i[0] for i in result.all()]


    async def get_one(self, **data) -> ACCOUNT | None:
        stmt = select(self.model).filter_by(**data, is_deleted=False)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.first()
        return res[0] if res else res

    async def filter_by_name_from_count(
        self, nameFilter: str, offset: int = 0, limit: int | None = None
    ) -> list[ACCOUNT] | None:
        stmt = (
            select(self.model)
            .filter(
                (self.model.firstName.like(f'%{nameFilter}%'))
                | (self.model.lastName.like(f'%{nameFilter}%'))
            )
            .offset(offset)
            .limit(limit)
            .filter_by(is_deleted=False)
        )

        res = await self.session.execute(stmt)  # type: ignore
        res = res.all()
        return [i[0] for i in res]


    async def offset(
        self, offset: int = 0, limit: int | None = None, order=None, **data
    ) -> list[ACCOUNT] | None:
        stmt = select(self.model).offset(offset).limit(limit).order_by(order).filter_by(**data, is_deleted=False)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.all()
        return [i[0] for i in res]