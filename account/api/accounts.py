from fastapi import APIRouter, Depends, Security, Query, Path

from core.schemas.account import SignUpSch, UpdateSch, AdminCreate
from core.services.account import AccountService
from core.enums import Roles
from core.exceptions import PermissionError
from account.schemas import AccessSch, AccessRefreshSch, AccountModelWithoutPassword

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
async def me(token=Security(get_token), uow=Depends(uowdep(account, lostoken))) -> AccountModelWithoutPassword:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    user = await AccountService(uow).me(int(access['id']))
    return AccountModelWithoutPassword(**user.model_dump())


@accountsR.put('/Update')
async def update(
    data: UpdateSch, token=Security(get_token), uow=Depends(uowdep(account, lostoken))
) -> AccountModelWithoutPassword:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    user = await AccountService(uow).update(int(access['id']), data)
    return AccountModelWithoutPassword(**user.model_dump())


@accountsR.get('/')
async def admin_get_accounts(
    count: int = Query(100, gt=0),
    from_: int = Query(0, alias='from', gt=-1),
    token=Security(get_token),
    uow=Depends(uowdep(account)),
) -> list[AccountModelWithoutPassword] | None:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise PermissionError('user not admin')
    u = await AccountService(uow).get_all(from_, count)
    return [AccountModelWithoutPassword(**i.model_dump()) for i in u]


@accountsR.get('/{id}')
async def get_account(
    id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account))
) -> AccountModelWithoutPassword | None:
    access = tokenSecure(token)
    u = await AccountService(uow).me(id)
    return AccountModelWithoutPassword(**u.model_dump()) if u else None


@accountsR.post('/')
async def admin_create(
    data: AdminCreate, token=Security(get_token), uow=Depends(uowdep(account))
) -> AccessRefreshSch:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise PermissionError('user not admin')
    user = await AccountService(uow).admin_create(data)
    access = accessCreate({'id': str(user.id)})
    refresh = refreshCreate({'id': str(user.id)})
    return {'accessToken': access, 'refreshToken': refresh}


@accountsR.put('/{id}')
async def admin_update(
    data: AdminCreate, id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account))
) -> AccountModelWithoutPassword:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise PermissionError('user not admin')
    user = await AccountService(uow).admin_update(id, data)
    return AccountModelWithoutPassword(**user.model_dump())


@accountsR.delete('/{id}')
async def admin_delete(id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account))) -> None:
    access = tokenSecure(token)

    user = await AccountService(uow).me(int(access['id']))
    if not Roles.ADMIN in user.roles:
        raise PermissionError('user not admin')
    user = await AccountService(uow).admin_delete(id)
    return user
