from core.infra.postgresql.tables import HOSPITAL
from core.repos.defaults.postgres import PostgresDefaultRepo
from core.repos.abstract import repo_logger
from sqlalchemy import delete, insert, select, update

@repo_logger
class HospitalRepo(PostgresDefaultRepo[HOSPITAL]):
    model = HOSPITAL
    reponame = 'hospital'

    async def get(self, **data) -> list[HOSPITAL] | None:
        result = await self.session.execute(
            select(self.model).order_by(self.model.id.desc()).filter_by(**data, is_deleted=False)
        )  # type: ignore
        return [i[0] for i in result.all()]


    async def get_one(self, **data) -> HOSPITAL | None:
        stmt = select(self.model).filter_by(**data, is_deleted=False)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.first()
        return res[0] if res else res


    async def offset(
        self, offset: int = 0, limit: int | None = None, order=None, **data
    ) -> list[HOSPITAL] | None:
        stmt = select(self.model).offset(offset).limit(limit).order_by(order).filter_by(**data, is_deleted=False)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.all()
        return [i[0] for i in res]