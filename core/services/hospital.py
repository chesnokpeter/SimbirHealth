from core.exceptions import NotFoundError
from core.models.hospital import HospitalModel
from core.schemas.hospital import CreateHospital
from core.services.abstract import AbsService, service_logger
from core.uow import uowaccess

@service_logger
class HospitalService(AbsService):
    @uowaccess('hospital')
    async def create(self, data: CreateHospital) -> HospitalModel:
        async with self.uow:
            h = await self.uow.hospital.add(**data.model_dump())
            await self.uow.commit()
            return h.model()

    @uowaccess('hospital')
    async def update(self, id: int, data: CreateHospital) -> HospitalModel:
        async with self.uow:
            exist = await self.uow.hospital.get_one(id=id)
            if not exist:
                raise NotFoundError('hospital does not found')

            h = await self.uow.hospital.update(id=id, **data.model_dump())
            await self.uow.commit()
            return h.model()

    @uowaccess('hospital')
    async def get_hospitals(self, from_: int, count: int) -> list[HospitalModel] | None:
        async with self.uow:
            h = await self.uow.hospital.offset(from_, count)
            return [i.model() for i in h]

    @uowaccess('hospital')
    async def get_hospital(self, id: int) -> HospitalModel | None:
        async with self.uow:
            h = await self.uow.hospital.get_one(id=id)
            return h.model() if h else None

    @uowaccess('hospital')
    async def delete(self, id: int) -> None:
        async with self.uow:
            await self.uow.hospital.update(id=id, is_deleted=True)
            await self.uow.commit()
            return None
