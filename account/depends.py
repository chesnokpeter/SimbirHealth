from datetime import timedelta, datetime, timezone
import jwt
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.exceptions import  HTTPException

from core.config import postgres_url, secret_key, redis_port, redis_host

from core.infra.postgresql import PostgresConnector
from core.infra.redis import RedisConnector
from core.repos.abstract import AbsRepo
from core.repos.account import AccountRepo
from core.repos.lostoken import LostokenRepo
from core.uow import UnitOfWork

from account.exceptions import JWTExceptions

# from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie

# access = JwtAccessBearerCookie(secret_key, False, access_expires_delta=timedelta(minutes=15))
# refresh = JwtRefreshBearerCookie(secret_key, False, refresh_expires_delta=timedelta(days=7))


# def accessSecure(a=Security(access)):
#     if not a:
#         raise JWTAccessExceptions(message='invalid jwt token')
#     return a


# def refreshSecure(a=Security(refresh)):
#     if not a:
#         raise JWTRefreshExceptions(message='invalid jwt token')
#     return a



def accessCreate(payload: dict[str, str]) -> str:
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=15) 
    return jwt.encode(payload, secret_key, algorithm='HS256')


def refreshCreate(payload: dict[str, str]) -> str:
    payload['exp'] = datetime.now(timezone.utc) + timedelta(days=7) 
    return jwt.encode(payload, secret_key, algorithm='HS256')


def tokenSecure(token: str) -> dict:
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise JWTExceptions(message='invalid jwt token')
    except jwt.InvalidTokenError:
        raise JWTExceptions(message='invalid jwt token')


postgres = PostgresConnector(postgres_url)
redis = RedisConnector(redis_host, redis_port)

connectors = [postgres]

account = AccountRepo()
lostoken = LostokenRepo()

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