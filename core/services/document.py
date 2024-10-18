from core.exceptions import NotFoundError, ConflictError, IncorrectError
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
                raise NotFoundError('user not found')
            if not Roles.USER in p.roles:
                raise IncorrectError('user not "user"')
            d = await self.uow.account.get_one(id=data.doctorId)
            if not d:
                raise NotFoundError('doctor not found')
            if not Roles.DOCTOR in d.roles:
                raise NotFoundError('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise NotFoundError('hospital not found')
            if not data.room in h.rooms:
                raise NotFoundError('no room at the hospital')

            date = data.date.replace(tzinfo=None)

            h = await self.uow.history.add(**data.model_dump(exclude=['date']), date=date)
            await self.uow.commit()
            return h.model()

    @uowaccess('history', 'account', 'hospital')
    async def update(self, id: int, data: CreateHistory) -> HistoryModel:
        async with self.uow:
            p = await self.uow.account.get_one(id=data.pacientId)
            if not p:
                raise NotFoundError('user not found')
            if not Roles.USER in p.roles:
                raise IncorrectError('user not "user"')
            d = await self.uow.account.get_one(id=data.doctorId)
            if not d:
                raise NotFoundError('doctor not found')
            if not Roles.DOCTOR in d.roles:
                raise NotFoundError('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise NotFoundError('hospital not found')
            if not data.room in h.rooms:
                raise NotFoundError('no room at the hospital')

            date = data.date.replace(tzinfo=None)

            h = await self.uow.history.update(id=id, **data.model_dump(exclude=['date']), date=date)
            await self.uow.commit()
            return h.model()

    @uowaccess('history')
    async def history_pacient(self, id: int) -> list[HistoryModel] | None:
        async with self.uow:
            h = await self.uow.history.get(pacientId=id)
            return [i.model() for i in h]

    @uowaccess('history')
    async def get_history(self, id: int) -> HistoryModel | None:
        async with self.uow:
            h = await self.uow.history.get_one(id=id)
            return h.model() if h else None
