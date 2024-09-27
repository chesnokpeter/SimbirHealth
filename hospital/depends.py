from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.exceptions import  HTTPException

from core.config import postgres_url, redis_port, redis_host

from core.models.account import AccountModel
from core.infra.postgresql import PostgresConnector
from core.infra.redis import RedisConnector
from core.repos.abstract import AbsRepo
from core.repos.hospital import HospitalRepo
from core.exceptions import RestExceptions
from core.uow import UnitOfWork


import httpx


postgres = PostgresConnector(postgres_url)
redis = RedisConnector(redis_host, redis_port)

connectors = [postgres]

hospital = HospitalRepo()

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