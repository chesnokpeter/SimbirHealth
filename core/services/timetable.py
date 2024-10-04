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
            if not u:
                raise AccountException('doctor not found')
            if not Roles.DOCTOR in u.roles:
                raise AccountException('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise HospitalException('hospital not found')
            if data.room not in h.rooms:
                raise HospitalException('no room at the hospital')

            from_dt = data.from_dt.replace(tzinfo=None)
            to_dt = data.to_dt.replace(tzinfo=None)

            t = await self.uow.timetable.add(**data.model_dump(exclude=['hospitalId', 'doctorId', 'from_dt', 'to_dt']), hospital_id=data.hospitalId, doctor_id=data.doctorId, from_dt=from_dt, to_dt=to_dt)
            await self.uow.commit()
            return t.model()
