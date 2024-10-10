from core.exceptions import DocumentException, AccountException, HospitalException
from core.models.history import HistoryModel
from core.schemas.history import CreateHistory
from core.services.abstract import AbsService
from core.enums import Roles
from core.uow import uowaccess



class DocumentService(AbsService):
    @uowaccess('history', 'account', 'hospital')
    async def create(self, data: CreateHistory) -> HistoryModel:
        async with self.uow:
            p = await self.uow.account.get_one(id=data.pacientId)
            if not p:
                raise AccountException('user not found')
            if not Roles.USER in p.roles:
                raise AccountException('user not "user"')
            d = await self.uow.account.get_one(id=data.doctorId)
            if not d:
                raise AccountException('doctor not found')
            if not Roles.DOCTOR in d.roles:
                raise AccountException('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise HospitalException('hospital not found')
            if not data.room in h.rooms:
                raise HospitalException('no room at the hospital')

            h = await self.uow.history.add(**data.model_dump())
            await self.uow.commit()
            return h.model()



    @uowaccess('history', 'account', 'hospital')
    async def update(self, id: int, data: CreateHistory) -> HistoryModel:
        async with self.uow:
            p = await self.uow.account.get_one(id=data.pacientId)
            if not p:
                raise AccountException('user not found')
            if not Roles.USER in p.roles:
                raise AccountException('user not "user"')
            d = await self.uow.account.get_one(id=data.doctorId)
            if not d:
                raise AccountException('doctor not found')
            if not Roles.DOCTOR in d.roles:
                raise AccountException('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise HospitalException('hospital not found')
            if not data.room in h.rooms:
                raise HospitalException('no room at the hospital')

            h = await self.uow.history.update(id=id, **data.model_dump())
            await self.uow.commit()
            return h.model()

