from core.infra.abstract import AbsConnector
from core.repos.types import RestConnType

import httpx

class RestAPIConnector(AbsConnector):
    connector_name = 'restapi'
    def clientret(self):
        return httpx.AsyncClient()

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def connect(self):
        client = self.clientret()
        self._session = RestConnType(client=client, baseurl=self.base_url)

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...

    @property
    def session(self):
        return self._session