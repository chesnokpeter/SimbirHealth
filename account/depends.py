from datetime import timedelta

from fastapi import Security

from core.config import postgres_url, secret_key

from core.infra.postgresql import PostgresConnector
from core.repos.abstract import AbsRepo
from core.repos.account import AccountRepo
from core.uow import UnitOfWork

from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie

from core.exceptions import JWTAccessExceptions, JWTRefreshExceptions

access = JwtAccessBearerCookie(secret_key, False, access_expires_delta=timedelta(minutes=15))
refresh = JwtRefreshBearerCookie(secret_key, False, refresh_expires_delta=timedelta(days=7))


def accessSecure(a=Security(access)):
    if not a:
        raise JWTAccessExceptions(message='invalid jwt token')
    return a


def refreshSecure(a=Security(refresh)):
    if not a:
        raise JWTRefreshExceptions(message='invalid jwt token')
    return a


postgres = PostgresConnector(postgres_url)

connectors = [postgres]

account = AccountRepo()


def uowdep(*repos: AbsRepo):
    connectors_name = {i.require_connector for i in repos}
    connectors_done = [i for i in connectors if i.connector_name in connectors_name]
    return lambda: UnitOfWork(repos, connectors_done)
