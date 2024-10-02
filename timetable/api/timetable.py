from fastapi import APIRouter, Depends, Security, Body, Query

# from core.schemas.account import SignUpSch, SignInSch, SignOutSch, UpdateSch, AdminCreate
# from core.services.account import AccountService
# from core.models.account import AccountModel
# from core.enums import Roles
# from core.exceptions import AccountException
# from account.schemas import AccessSch, AccessRefreshSch

timetableR = APIRouter(prefix='/Timetable', tags=['Timetable'])


@timetableR.post('/')
async def new_timetable():
    return