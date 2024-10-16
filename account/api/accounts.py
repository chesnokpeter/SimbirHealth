from fastapi import APIRouter, Depends, Security, Query, Path

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
    get_token,
)


@accountsR.get('/Me')
async def me(token=Security(get_token), uow=Depends(uowdep(account, lostoken))) -> SignUpSch:
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
    user = await AccountService(uow).update(int(access['id']), data)
    return SignUpSch(**user.model_dump())


@accountsR.get('/')
async def admin_get_accounts(
    count: int = Query(100, gt=0),
    from_: int = Query(0, alias='from', gt=-1),
    token=Security(get_token),
    uow=Depends(uowdep(account)),
) -> list[AccountModel] | None:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise AccountException('user not admin')
    u = await AccountService(uow).get_all(from_, count)
    return u


@accountsR.get('/{id}')
async def get_account(
    id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account))
) -> AccountModel | None:
    access = tokenSecure(token)
    u = await AccountService(uow).me(id)
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
    return {'accessToken': access, 'refreshToken': refresh}


@accountsR.put('/{id}')
async def admin_update(
    data: AdminCreate, id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account))
) -> AccountModel:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise AccountException('user not admin')
    user = await AccountService(uow).admin_update(id, data)
    return user


@accountsR.delete('/{id}')
async def admin_delete(id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account))) -> None:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise AccountException('user not admin')
    user = await AccountService(uow).admin_delete(id)
    return user
