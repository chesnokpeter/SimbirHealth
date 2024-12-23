from fastapi import APIRouter, Depends, Security, Body, Query, Path

from core.services.account import AccountService
from account.schemas import AccountModelWithoutPassword
doctorsR = APIRouter(prefix='/Doctors', tags=['Doctors'])

from account.depends import account, lostoken, uowdep, tokenSecure, get_token


@doctorsR.get('/')
async def get_doctors(
    nameFilter: str,
    count: int = Query(100, gt=0),
    from_: int = Query(0, alias='from', gt=-1),
    token=Security(get_token),
    uow=Depends(uowdep(account, lostoken)),
) -> list[AccountModelWithoutPassword] | None:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    await AccountService(uow).me(int(access['id']))

    u = await AccountService(uow).get_doctors(nameFilter, from_, count)
    return [AccountModelWithoutPassword(**i.model_dump()) for i in u]


@doctorsR.get('/{id}')
async def get_doctor(id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account, lostoken))) -> AccountModelWithoutPassword | None:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    await AccountService(uow).me(int(access['id']))

    u = await AccountService(uow).get_doctor(id)
    return AccountModelWithoutPassword(**u.model_dump()) if u else None
