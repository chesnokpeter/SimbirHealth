from core.exceptions import TimetableException, AccountException, HospitalException
from core.models.timetable import TimetableModel
from core.enums import Roles
from core.schemas.timetable import TimetableCreate
from core.services.abstract import AbsService
from core.uow import uowaccess



class TimetableService(AbsService):
    @uowaccess('timetable', 'account', 'hospital')
    async def create(self, data: TimetableCreate) -> TimetableModel:
        async with self.uow:
            u = await self.uow.account.get_one(id=data.doctorId)
            print(u)
            if not u:
                raise AccountException('doctor not found')
            if not Roles.DOCTOR in u.roles:
                raise AccountException('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise HospitalException('hospital not found')

            t = await self.uow.timetable.add(**data.model_dump(exclude=['hospitalId', 'doctorId']), hospital_id=data.hospitalId, doctor_id=data.doctorId)
            await self.uow.commit()
            return t.model()
    #!ПРОВЕРИТЬ НАЛИЧИЕ КОМНАТЫ В БОЛЬНИЦЕ

    '''
    qlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $3: datetime.datetime(2024, 4, 25, 11, 30, t... (can't subtract offset-naive and offset-aware datetimes)
[SQL: INSERT INTO timetable (hospital_id, doctor_id, from_dt, to_dt, room) VALUES ($1::INTEGER, $2::INTEGER, $3::TIMESTAMP WITHOUT TIME ZONE, $4::TIMESTAMP WITHOUT TIME ZONE, $5::VARCHAR) RETURNING timetable.id, timetable.hospital_id, timetable.doctor_id, timetable.from_dt, timetable.to_dt, timetable.room]
[parameters: (2, 7, datetime.datetime(2024, 4, 25, 11, 30, tzinfo=TzInfo(UTC)), datetime.datetime(2024, 4, 25, 12, 0, tzinfo=TzInfo(UTC)), 'string')]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
'''