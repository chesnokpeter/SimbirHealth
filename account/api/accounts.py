from fastapi import APIRouter, Depends, Security, Body, Query

from core.schemas.account import SignUpSch, SignInSch, SignOutSch, UpdateSch, AdminCreate
from core.services.account import AccountService
from core.models.account import AccountModel
from core.enums import Roles
from core.exceptions import AccountException
from account.schemas import AccessSch, AccessRefreshSch

accountsR = APIRouter(prefix='/Accounts', tags=['Accounts'])

from account.depends import (
    account,
    lostoken,
    uowdep,
    accessCreate,
    refreshCreate,
    tokenSecure,
    get_token
)


@accountsR.get('/Me')
async def me(
        token=Security(get_token), uow=Depends(uowdep(account, lostoken))
    ) -> SignUpSch:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    user = await AccountService(uow).me(int(access['id']))
    return SignUpSch(**user.model_dump())

@accountsR.put('/Update')
async def update(
        data: UpdateSch, token=Security(get_token), uow=Depends(uowdep(account, lostoken))
    ) -> SignUpSch:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    await AccountService(uow).me(int(access['id']))
    user = await AccountService(uow).update(int(access['id']), data)
    return SignUpSch(**user.model_dump())

@accountsR.get('/')
async def get_accounts(
        count: int, from_ : int = Query(0, alias='from'), token=Security(get_token), uow=Depends(uowdep(account))
    ) -> list[AccountModel] | None:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise AccountException('user not admin')
    u = await AccountService(uow).get_all(from_, count) 
    return u


@accountsR.post('/')
async def admin_create(
        data: AdminCreate, token=Security(get_token), uow=Depends(uowdep(account))
    ) -> AccessRefreshSch:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise AccountException('user not admin')
    user = await AccountService(uow).admin_create(data)
    access = accessCreate({'id': str(user.id)})
    refresh = refreshCreate({'id': str(user.id)})
    return {'accessToken':access, 'refreshToken':refresh}