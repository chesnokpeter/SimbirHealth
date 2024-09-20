from fastapi import APIRouter, Depends, Security, Body

from core.schemas.account import SignUpSch, SignIn
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
async def signup(data: SignUpSch, uow=Depends(uowdep(account))):
    user = await AccountService(uow).signup(data)
    access_token = access.create_access_token(subject={'id': user.id})
    refresh_token = refresh.create_refresh_token(subject={'id': user.id})
    return {'accessToken':access_token, 'refreshToken':refresh_token}


@authenticationR.post('/SignIn')
async def signin(data: SignIn, uow=Depends(uowdep(account))):
    user = await AccountService(uow).signin(data)
    access_token = access.create_access_token(subject={'id': user.id})
    refresh_token = refresh.create_refresh_token(subject={'id': user.id})
    return {'accessToken':access_token, 'refreshToken':refresh_token}
