from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import postgres_url

from core.models.account import AccountModel
from core.infra.postgresql import PostgresConnector
from core.repos.abstract import AbsRepo
from core.repos.timetable import TimetableRepo
from core.repos.appointment import AppointmentRepo
from core.uow import UnitOfWork
from timetable.customrepos import RestDoctorRepo, RestRoomsRepo
from timetable.customconnectors import RestAPIConnector
from timetable.exceptions import JWTExceptions


import httpx


postgres = PostgresConnector(postgres_url)
restapiaccount = RestAPIConnector(base_url='http://account:', connector_name='restapiaccount')
restapihospital = RestAPIConnector(base_url='http://hospital:', connector_name='restapihospital')

connectors = [postgres, restapiaccount, restapihospital]

timetable = TimetableRepo()

appointment = AppointmentRepo()


def get_timetrepo():
    return timetable


def get_apporepo():
    return appointment


def uowdep(*repos: AbsRepo):
    connectors_name = {i.require_connector for i in repos}
    connectors_done = [i for i in connectors if i.connector_name in connectors_name]
    return lambda: UnitOfWork(repos, connectors_done)


secure = HTTPBearer(auto_error=False)

def get_token(credentials: HTTPAuthorizationCredentials = Security(secure)) -> str:
    if not credentials:
        raise JWTExceptions(message='not authenticated')
    if credentials.scheme != 'Bearer':
        raise JWTExceptions(message='invalid authentication scheme')

    token = credentials.credentials
    return token


async def introspection(token: str) -> AccountModel:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            'http://account:8011/api/Authentication/Validate', params={'accessToken': token}
        )
        r = r.json()
        if r.get('error'):
            raise JWTExceptions('invalid jwt token')
        try:
            u = AccountModel(**r)
            return u
        except:
            raise JWTExceptions('invalid jwt token')


def get_accrepo(token: str):
    return RestDoctorRepo('restapiaccount', token)


def get_hosrepo(token: str):
    return RestRoomsRepo('restapihospital', token)
