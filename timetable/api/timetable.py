from fastapi import APIRouter, Depends, Security, Body, Query

from core.services.timetable import TimetableService
from core.schemas.timetable import TimetableCreate, AppointmentsCreate
from core.models.timetable import TimetableModel
from core.models.appoiniment import AppoinimentModel
from core.exceptions import AccountException
from core.enums import Roles

from timetable.depends import (
    get_accrepo,
    get_hosrepo,
    uowdep,
    get_token,
    introspection,
    get_timetrepo,
    get_apporepo,
)
from timetable.schemas import AvailableAppointments

from datetime import datetime

timetableR = APIRouter(prefix='/Timetable', tags=['Timetable'])


@timetableR.post('/')
async def new_timetable(
    data: TimetableCreate, token=Security(get_token), tt=Depends(get_timetrepo)
) -> TimetableModel:
    u = await introspection(token)
    if not (Roles.ADMIN or Roles.MANAGER in u.roles):
        raise AccountException('user not admin or manager')
    uow = uowdep(tt, get_accrepo(token), get_hosrepo(token))()
    t = await TimetableService(uow).create(data)
    return t


@timetableR.put('/{id}')
async def upd_timetable(
    id: int, data: TimetableCreate, token=Security(get_token), tt=Depends(get_timetrepo)
) -> TimetableModel:
    u = await introspection(token)
    if not (Roles.ADMIN or Roles.MANAGER in u.roles):
        raise AccountException('user not admin or manager')
    uow = uowdep(tt, get_accrepo(token), get_hosrepo(token))()
    t = await TimetableService(uow).update(id, data)
    return t


@timetableR.delete('/{id}')
async def del_timetable(id: int, token=Security(get_token), tt=Depends(get_timetrepo)) -> None:
    u = await introspection(token)
    if not (Roles.ADMIN or Roles.MANAGER in u.roles):
        raise AccountException('user not admin or manager')
    uow = uowdep(tt)()
    t = await TimetableService(uow).delete(id)
    return t


@timetableR.delete('/Doctor/{id}')
async def del_from_doctor(id: int, token=Security(get_token), tt=Depends(get_timetrepo)) -> None:
    u = await introspection(token)
    if not (Roles.ADMIN or Roles.MANAGER in u.roles):
        raise AccountException('user not admin or manager')
    uow = uowdep(tt)()
    t = await TimetableService(uow).delete_from_doctor(id)
    return t


@timetableR.delete('/Hospital/{id}')
async def del_from_hospital(id: int, token=Security(get_token), tt=Depends(get_timetrepo)) -> None:
    u = await introspection(token)
    if not (Roles.ADMIN or Roles.MANAGER in u.roles):
        raise AccountException('user not admin or manager')
    uow = uowdep(tt)()
    t = await TimetableService(uow).delete_from_hospital(id)
    return t


@timetableR.get('/Hospital/{id}')
async def get_timetable_from_hospital(
    id: int,
    to: datetime,
    from_: datetime = Query(alias='from'),
    token=Security(get_token),
    tt=Depends(get_timetrepo),
) -> list[TimetableModel]:
    u = await introspection(token)
    uow = uowdep(tt)()
    t = await TimetableService(uow).timetable_from_hospital(id, to, from_)
    return t


@timetableR.get('/Doctor/{id}')
async def get_timetable_from_doctor(
    id: int,
    to: datetime,
    from_: datetime = Query(alias='from'),
    token=Security(get_token),
    tt=Depends(get_timetrepo),
) -> list[TimetableModel]:
    u = await introspection(token)
    uow = uowdep(tt)()
    t = await TimetableService(uow).timetable_from_doctor(id, to, from_)
    return t


@timetableR.get('/Hospital/{id}/Room/{room}')
async def get_timetable_from_hospital_room(
    id: int,
    room: str,
    to: datetime,
    from_: datetime = Query(alias='from'),
    token=Security(get_token),
    tt=Depends(get_timetrepo),
) -> list[TimetableModel]:
    u = await introspection(token)
    if not (Roles.ADMIN or Roles.MANAGER or Roles.DOCTOR in u.roles):
        raise AccountException('user not admin or manager or doctor')
    uow = uowdep(tt)()
    t = await TimetableService(uow).timetable_from_room(id, room, to, from_)
    return t


@timetableR.post('/{id}/Appointments')
async def create_appointments(
    id: int,
    data: AppointmentsCreate,
    token=Security(get_token),
    tt=Depends(get_timetrepo),
    at=Depends(get_apporepo),
) -> AppoinimentModel:
    u = await introspection(token)
    uow = uowdep(tt, at)()
    t = await TimetableService(uow).create_appointments(id, data, u.id)
    return t


@timetableR.get('/{id}/Appointments')
async def get_available_appointments(
    id: int, token=Security(get_token), tt=Depends(get_timetrepo), at=Depends(get_apporepo)
) -> AvailableAppointments:
    u = await introspection(token)
    uow = uowdep(tt, at)()
    t = await TimetableService(uow).get_appointments(id)
    return AvailableAppointments(appointments=t)
