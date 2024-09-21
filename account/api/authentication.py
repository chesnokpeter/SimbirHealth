from fastapi import APIRouter, Depends, Security, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.schemas.account import SignUpSch, SignIn, SignOut
from core.services.account import AccountService

authenticationR = APIRouter(prefix='/Authentication', tags=['Authentication'])

from account.depends import (
    account,
    lostoken,
    uowdep,
    accessCreate,
    refreshCreate,
    tokenSecure
)


@authenticationR.post('/SignUp')
async def signup(data: SignUpSch, uow=Depends(uowdep(account))):
    user = await AccountService(uow).signup(data)
    access = accessCreate({'id': str(user.id)})
    refresh = refreshCreate({'id': str(user.id)})
    return {'accessToken':access, 'refreshToken':refresh}


@authenticationR.post('/SignIn')
async def signin(data: SignIn, uow=Depends(uowdep(account))):
    user = await AccountService(uow).signin(data)
    access = accessCreate({'id': str(user.id)})
    refresh = refreshCreate({'id': str(user.id)})
    return {'accessToken':access, 'refreshToken':refresh}


@authenticationR.put('/SignOut')
async def signout(
        data: SignOut,
        uow=Depends(uowdep(lostoken))
    ):
    await AccountService(uow).signout(data)


@authenticationR.get('/Validate')
async def validate_token(
        accessToken: str, uow=Depends(uowdep(account, lostoken))
    ):
    access = tokenSecure(accessToken)
    await AccountService(uow).checklostoken(accessToken)
    user = await AccountService(uow).me(int(access['id']))
    return user


@authenticationR.post('/Refresh')
async def refresh_token(
        refreshToken: str = Body(embed=True), uow=Depends(uowdep(account))
    ):
    refresh = tokenSecure(refreshToken)

    user = await AccountService(uow).me(int(refresh['id']))
    access = accessCreate({'id': str(user.id)})
    return {'accessToken':access}


