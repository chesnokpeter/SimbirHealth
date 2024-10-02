from core.repos.abstract import AbsRepo
from core.models.account import AccountModel
from core.models.hospital import HospitalModel
from core.repos.types import RestConnType


class RestDoctorRepo(AbsRepo[RestConnType]):
    model: AccountModel
    reponame = 'account'
    async def get_one(self, id: int) -> AccountModel | None:
        d = await self.session.client.get(f'{self.session.baseurl}/Doctors/{id}')
        d = d.json()
        if not d:
            return None
        return AccountModel(**d)



class RestRoomsRepo(AbsRepo[RestConnType]):
    model: HospitalModel
    reponame = 'hospital'
    async def get_one(self, id: int) -> HospitalModel | None:
        d = await self.session.client.get(f'{self.session.baseurl}/Hospitals/{id}/Rooms/')
        d = d.json()
        if not d:
            return None
        return HospitalModel(**d)
    
    