from datetime import timedelta, datetime, timezone
import jwt
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.exceptions import HTTPException

from core.config import postgres_url, secret_key

from core.infra.postgresql import PostgresConnector
from core.repos.abstract import AbsRepo
from core.repos.account import AccountRepo
from core.repos.lostoken import LostokenRepo
from core.uow import UnitOfWork

from account.exceptions import JWTExceptions


def accessCreate(payload: dict[str, str]) -> str:
    payload['exp'] = datetime.now(timezone.utc) + timedelta(hours=1)
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
    except:
        raise JWTExceptions(message='invalid jwt token')


postgres = PostgresConnector(postgres_url)

connectors = [postgres]

account = AccountRepo()
lostoken = LostokenRepo()


def uowdep(*repos: AbsRepo):
    connectors_name = {i.require_connector for i in repos}
    connectors_done = [i for i in connectors if i.connector_name in connectors_name]
    return lambda: UnitOfWork(repos, connectors_done)


secure = HTTPBearer(auto_error=False)


def get_token(credentials: HTTPAuthorizationCredentials = Security(secure)) -> str:
    if not credentials:
        raise JWTExceptions(message='not authenticated')
    if credentials.scheme != 'Bearer':
        raise JWTExceptions(detail='invalid authentication scheme')

    token = credentials.credentials
    return token
