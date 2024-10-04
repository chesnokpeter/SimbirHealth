from fastapi import APIRouter, Depends, Security, Body, Query

from core.services.timetable import TimetableService
from core.schemas.timetable import TimetableCreate
from core.models.timetable import TimetableModel
from core.exceptions import AccountException
from core.enums import Roles

from timetable.depends import (
    get_accrepo,
    get_hosrepo, 
    uowdep,
    get_token, 
    introspection,
    get_timetrepo
)

timetableR = APIRouter(prefix='/Timetable', tags=['Timetable'])


@timetableR.post('/')
async def new_timetable(
    data: TimetableCreate, token=Security(get_token), tt=Depends(get_timetrepo)
) -> TimetableModel:
    u = await introspection(token)
    if not Roles.ADMIN in u.roles:
        raise AccountException('user not admin')
    uow = uowdep(tt, get_accrepo(token), get_hosrepo(token))()
    t = await TimetableService(uow).create(data)
    return t