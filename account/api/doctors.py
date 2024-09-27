from fastapi import APIRouter, Depends, Security, Body, Query

from core.schemas.account import SignUpSch, SignInSch, SignOutSch, UpdateSch, AdminCreate
from core.services.account import AccountService
from core.models.account import AccountModel
from core.enums import Roles
from core.exceptions import AccountException
from account.schemas import AccessSch, AccessRefreshSch

doctorsR = APIRouter(prefix='/Doctors', tags=['Doctors'])

from account.depends import (
    account,
    lostoken,
    uowdep,
    tokenSecure,
    get_token
)

@doctorsR.get('/')
async def get_doctors(
        nameFilter: str, count: int=100, from_ : int = Query(0, alias='from'), token=Security(get_token), uow=Depends(uowdep(account, lostoken))
    ) -> list[AccountModel] | None:
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    await AccountService(uow).me(int(access['id']))

    u = await AccountService(uow).get_doctors(nameFilter, from_, count) 
    return u

@doctorsR.get('/{id}') #!ДОПИСАТЬ
async def get_doctor(
        id : int, token=Security(get_token), uow=Depends(uowdep(account, lostoken))
    ):
    access = tokenSecure(token)
    await AccountService(uow).checklostoken(token)
    await AccountService(uow).me(int(access['id']))

    u = await AccountService(uow).get_doctor(id) 
    return u



