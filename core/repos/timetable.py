from core.infra.postgresql.tables import TIMETABLE
from core.repos.defaults.postgres import PostgresDefaultRepo

from sqlalchemy import select
from sqlalchemy.sql.expression import and_
from datetime import datetime


class TimetableRepo(PostgresDefaultRepo[TIMETABLE]):
    model = TIMETABLE
    reponame = 'timetable'

    async def get_by_time_range(
        self, from_: datetime, to: datetime, **filters
    ) -> list[TIMETABLE] | None:
        stmt = (
            select(self.model)
            .filter(and_(self.model.from_dt >= from_, self.model.to_dt <= to))
            .filter_by(**filters)
        )

        result = await self.session.execute(stmt)  # type: ignore
        records = result.all()

        return [record[0] for record in records] if records else None
