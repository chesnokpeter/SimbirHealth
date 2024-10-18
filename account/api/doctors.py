from fastapi import APIRouter, Depends, Security, Body, Query, Path

from core.services.account import AccountService
from core.models.account import AccountModel

doctorsR = APIRouter(prefix='/Doctors', tags=['Doctors'])

from account.depends import account, lostoken, uowdep, tokenSecure, get_token


@doctorsR.get('/')
async def get_doctors(
    nameFilter: str,
    count: int = Query(100, gt=0),
    from_: int = Query(0, alias='from', gt=-1),
    token=Security(get_token),
    uow=Depends(uowdep(account, lostoken)),
) -> list[AccountModel] | None:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    await AccountService(uow).me(int(access['id']))

    u = await AccountService(uow).get_doctors(nameFilter, from_, count)
    return u


@doctorsR.get('/{id}')
async def get_doctor(id: int = Path(gt=0), token=Security(get_token), uow=Depends(uowdep(account, lostoken))):
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    await AccountService(uow).me(int(access['id']))

    u = await AccountService(uow).get_doctor(id)
    return u
