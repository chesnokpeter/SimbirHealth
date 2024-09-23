from core.infra.postgresql.tables import ACCOUNT
from core.repos.defaults.postgres import PostgresDefaultRepo
from sqlalchemy import delete, insert, select, update


class AccountRepo(PostgresDefaultRepo[ACCOUNT]):
    model = ACCOUNT
    reponame = 'account'
    async def get(self, **data) -> list[ACCOUNT] | None:

        result = await self.session.execute(
            select(self.model).order_by(self.model.id.desc()).filter_by(**data)
        )  # type: ignore
        return [i[0] for i in result.all() if not i[0].is_deleted]

    async def get_one(self, **data) -> ACCOUNT | None:
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.first()
        return res[0] if res[0] else res