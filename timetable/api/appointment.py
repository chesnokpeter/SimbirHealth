from fastapi import APIRouter, Depends, Security, Body, Query, Path

from core.services.timetable import TimetableService
from core.exceptions import AccountException
from core.enums import Roles

from timetable.depends import uowdep, get_token, introspection, get_apporepo

appointmenteR = APIRouter(prefix='/Appointment', tags=['Appointment'])


@appointmenteR.delete('/{id}')
async def del_appointment(id: int = Path(gt=0), token=Security(get_token), at=Depends(get_apporepo)) -> None:
    u = await introspection(token)
    uow = uowdep(at)()
    a = await TimetableService(uow).get_appointment(id)
    if not (Roles.ADMIN or Roles.MANAGER in u.roles or u.id != a.patient_id):
        raise AccountException('user not admin or manager or not patient this appointment')
    t = await TimetableService(uow).del_appointment(id)
    return t
