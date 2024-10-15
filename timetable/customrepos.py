from core.repos.abstract import AbsRepo
from core.models.account import AccountModel
from core.models.hospital import HospitalModel
from core.repos.types import RestConnType

import httpx


class BearerAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        yield request


class RestDoctorRepo(AbsRepo[RestConnType]):
    model: AccountModel
    reponame = 'account'

    def __init__(self, require_connector: str, token: str):
        super().__init__(require_connector)
        self.token = token

    async def get_one(self, id: int) -> AccountModel | None:
        auth = BearerAuth(self.token)
        d = await self.session.client.get(f'{self.session.baseurl}8011/api/Doctors/{id}', auth=auth)
        d = d.json()
        if not d or d.get('error'):
            return None
        return AccountModel(**d)


class RestRoomsRepo(AbsRepo[RestConnType]):
    model: HospitalModel
    reponame = 'hospital'

    def __init__(self, require_connector: str, token: str):
        super().__init__(require_connector)
        self.token = token

    async def get_one(self, id: int) -> HospitalModel | None:
        auth = BearerAuth(self.token)
        d = await self.session.client.get(
            f'{self.session.baseurl}8021/api/Hospitals/{id}', auth=auth
        )
        d = d.json()
        if not d or d.get('error'):
            return None
        return HospitalModel(**d)
