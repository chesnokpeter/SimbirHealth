from fastapi import APIRouter, Depends, Security, Body, Query

from core.schemas.account import SignUpSch, SignInSch, SignOutSch
from core.services.account import AccountService
from core.models.account import AccountModel
from account.schemas import AccessSch, AccessRefreshSch

authenticationR = APIRouter(prefix='/Authentication', tags=['Authentication'])

from account.depends import (
    account,
    lostoken,
    uowdep,
    accessCreate,
    refreshCreate,
    tokenSecure,
    get_token
)


@authenticationR.post('/SignUp')
async def signup(data: SignUpSch, uow=Depends(uowdep(account))) -> AccessRefreshSch:
    user = await AccountService(uow).signup(data)
    access = accessCreate({'id': str(user.id)})
    refresh = refreshCreate({'id': str(user.id)})
    return {'accessToken': access, 'refreshToken': refresh}


@authenticationR.post('/SignIn')
async def signin(data: SignInSch, uow=Depends(uowdep(account))) -> AccessRefreshSch:
    user = await AccountService(uow).signin(data)
    access = accessCreate({'id': str(user.id)})
    refresh = refreshCreate({'id': str(user.id)})
    return {'accessToken': access, 'refreshToken': refresh}


@authenticationR.put('/SignOut')
async def signout(data: SignOutSch, uow=Depends(uowdep(lostoken))) -> None:
    await AccountService(uow).signout(data)


@authenticationR.get('/Validate')
async def validate_token(accessToken: str, uow=Depends(uowdep(account, lostoken))) -> AccountModel:
    access = tokenSecure(accessToken)
    await AccountService(uow).checklostoken(accessToken)
    user = await AccountService(uow).me(int(access['id']))
    return user


@authenticationR.post('/Refresh')
async def refresh_token(
    refreshToken: str = Body(embed=True), uow=Depends(uowdep(account, lostoken))
) -> AccessSch:
    refresh = tokenSecure(refreshToken, refresh=True)
    await AccountService(uow).checklostoken(refreshToken=refreshToken)
    user = await AccountService(uow).me(int(refresh['id']))
    access = accessCreate({'id': str(user.id)})
    return {'accessToken': access}
