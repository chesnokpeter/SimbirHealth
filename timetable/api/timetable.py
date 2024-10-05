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
    if not Roles.ADMIN or Roles.MANAGER in u.roles:
        raise AccountException('user not admin or manager')
    uow = uowdep(tt, get_accrepo(token), get_hosrepo(token))()
    t = await TimetableService(uow).create(data)
    return t

@timetableR.put('/{id}')
async def upd_timetable(
    id: int, data: TimetableCreate, token=Security(get_token), tt=Depends(get_timetrepo)
) -> TimetableModel:
    u = await introspection(token)
    if not Roles.ADMIN or Roles.MANAGER in u.roles:
        raise AccountException('user not admin or manager')
    uow = uowdep(tt, get_accrepo(token), get_hosrepo(token))()
    t = await TimetableService(uow).update(id, data)
    return t

@timetableR.delete('/{id}')
async def del_timetable(
    id: int, token=Security(get_token), tt=Depends(get_timetrepo)
) -> TimetableModel:
    u = await introspection(token)
    if not Roles.ADMIN or Roles.MANAGER in u.roles:
        raise AccountException('user not admin or manager')
    uow = uowdep(tt, get_accrepo(token), get_hosrepo(token))()
    t = await TimetableService(uow).delete(id)
    return t


@app.get("/api/Timetable/{id}/Appointments")
def get_available_appointments(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    timetable = db.query(TIMETABLE).filter(TIMETABLE.id == id).first()
    
    if not timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")

    from_time = timetable.from_dt
    to_time = timetable.to_dt

    slot_duration = timedelta(minutes=30)
    current_slot = from_time
    available_slots = []

    while current_slot < to_time:
        appointment_exists = db.query(APPOINTMENT).filter(
            and_(
                APPOINTMENT.timetable_id == id,
                APPOINTMENT.time == current_slot
            )
        ).first()

        if not appointment_exists:
            available_slots.append(current_slot)

        current_slot += slot_duration

    return {"available_appointments": available_slots}


@app.post("/api/Timetable/{id}/Appointments")
def book_appointment(id: int, appointment_request: AppointmentRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    timetable = db.query(TIMETABLE).filter(TIMETABLE.id == id).first()

    if not timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")
    
    requested_time = appointment_request.time

    if requested_time < timetable.from_dt or requested_time >= timetable.to_dt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment time outside timetable range")

    time_diff = requested_time - timetable.from_dt
    if time_diff.total_seconds() % (30 * 60) != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment time must be in 30-minute intervals")

    appointment_exists = db.query(APPOINTMENT).filter(
        and_(
            APPOINTMENT.timetable_id == id,
            APPOINTMENT.time == requested_time
        )
    ).first()

    if appointment_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Time slot already booked")

    new_appointment = APPOINTMENT(
        time=requested_time,
        timetable_id=timetable.id,
        patient_id=current_user['id'] 
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {"message": "Appointment booked successfully", "appointment_id": new_appointment.id}