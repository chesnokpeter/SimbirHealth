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
            if not u or not Roles.DOCTOR in u.roles:
                raise AccountException('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise HospitalException('hospital not found')

            t = await self.uow.timetable.add(**data.model_dump())
            await self.uow.commit()
            return t.model()
