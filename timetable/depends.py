from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.exceptions import  HTTPException

from core.config import postgres_url

from core.models.account import AccountModel
from core.infra.postgresql import PostgresConnector
from core.repos.abstract import AbsRepo
from core.repos.timetable import TimetableRepo
from core.exceptions import RestExceptions
from core.uow import UnitOfWork
from timetable.repos import RestDoctorRepo, RestRoomsRepo
from timetable.connectors import RestAPIConnector

import httpx


postgres = PostgresConnector(postgres_url)
restapi = RestAPIConnector(base_url='http://127.0.0.1:')

connectors = [postgres, restapi]

timetable = TimetableRepo()

def get_timetrepo(): return timetable

def uowdep(*repos: AbsRepo):
    connectors_name = {i.require_connector for i in repos}
    connectors_done = [i for i in connectors if i.connector_name in connectors_name]
    return lambda: UnitOfWork(repos, connectors_done)

secure = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Security(secure)):
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=401,
            detail="invalid authentication scheme"
        )
    
    token = credentials.credentials
    return token

async def introspection(token: str) -> AccountModel:
    async with httpx.AsyncClient() as client:
        r = await client.get('http://localhost:8011/api/Authentication/Validate', params={'accessToken':token})
        r = r.json()
        if r.get('error'): raise RestExceptions('invalid jwt token')
        try:
            u = AccountModel(**r)
            return u
        except: raise RestExceptions('invalid jwt token')

def get_accrepo(token: str):
    return RestDoctorRepo('restapi', token)

def get_hosrepo(token: str):
    return RestRoomsRepo('restapi', token)