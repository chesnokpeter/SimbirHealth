from core.infra.postgresql.tables import HOSPITAL
from core.repos.defaults.postgres import PostgresDefaultRepo

from sqlalchemy import delete, insert, select, update

class HospitalRepo(PostgresDefaultRepo[HOSPITAL]):
    model = HOSPITAL
    reponame = 'hospital'
    async def get(self, **data) -> list[HOSPITAL] | None:
        result = await self.session.execute(
            select(self.model).order_by(self.model.id.desc()).filter_by(**data)
        )  # type: ignore
        filtered_results = []
        for i in result.all():
            if not i[0].is_deleted:
                filtered_results.append(i[0])

    async def get_one(self, **data) -> HOSPITAL | None:
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.first()
        if res:
            if not res[0].is_deleted:
                result = res[0]
            else:
                result = None
        else:
            result = res
        return result
    
    async def offset(
        self, offset: int = 0, limit: int | None = None, order=None, **data
    ) -> list[HOSPITAL] | None:
        stmt = select(self.model).offset(offset).limit(limit).order_by(order).filter_by(**data)
        res = await self.session.execute(stmt)  # type: ignore
        res = res.all()
        filtered_results = []
        for i in res:
            if not i[0].is_deleted:
                filtered_results.append(i[0])
        return filtered_results