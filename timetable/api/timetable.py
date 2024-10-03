from fastapi import APIRouter, Depends, Security, Body, Query

from core.services.timetable import TimetableService
from core.schemas.timetable import TimetableCreate

from timetable.depends import (
    timetable, 
    get_accrepo,
    get_hosrepo, 
    uowdep,
    get_token, 
    introspection
)

timetableR = APIRouter(prefix='/Timetable', tags=['Timetable'])


@timetableR.post('/')
async def new_timetable(
    data: TimetableCreate, token=Security(get_token), tt=timetable
):
    await introspection(token)
    uow=uowdep(tt, get_accrepo(token), get_hosrepo(token))()
    t = await TimetableService(uow).create(data)
    return t