from fastapi import APIRouter, Depends, Security, Body

from core.schemas.account import SignUpSch
from core.services.account import AccountService

authenticationR = APIRouter(prefix='/Authentication', tags=['Authentication'])

from account.depends import (
    account,
    access,
    accessSecure,
    refresh,
    refreshSecure,
    uowdep,
)

@authenticationR.post('/SignUp')
async def signup_user(data: SignUpSch, uow=Depends(uowdep(account))):
    user = await AccountService(uow).signup(data)

    access_token = access.create_access_token(subject={'id': user.id})
    refresh_token = refresh.create_refresh_token(subject={'id': user.id})



    return access_token, refresh_token