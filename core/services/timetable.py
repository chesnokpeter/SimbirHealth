from core.exceptions import TimetableException, AccountException, HospitalException
from core.models.timetable import TimetableModel
from core.enums import Roles
from core.schemas.timetable import TimetableCreate, AppointmentsCreate
from core.models.appoiniment import AppoinimentModel
from core.services.abstract import AbsService
from core.uow import uowaccess

from datetime import timezone, timedelta, datetime


class TimetableService(AbsService):
    @uowaccess('timetable', 'account', 'hospital')
    async def create(self, data: TimetableCreate) -> TimetableModel:
        async with self.uow:
            u = await self.uow.account.get_one(id=data.doctorId)
            if not u:
                raise AccountException('doctor not found')
            if not Roles.DOCTOR in u.roles:
                raise AccountException('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise HospitalException('hospital not found')
            if data.room not in h.rooms:
                raise HospitalException('no room at the hospital')

            from_dt = data.from_dt.replace(tzinfo=None)
            to_dt = data.to_dt.replace(tzinfo=None)

            t = await self.uow.timetable.add(
                **data.model_dump(exclude=['hospitalId', 'doctorId', 'from_dt', 'to_dt']),
                hospital_id=data.hospitalId,
                doctor_id=data.doctorId,
                from_dt=from_dt,
                to_dt=to_dt,
            )
            await self.uow.commit()
            return t.model()

    @uowaccess('timetable', 'account', 'hospital')
    async def update(self, id: int, data: TimetableCreate) -> TimetableModel:
        async with self.uow:
            t = await self.uow.timetable.get_one(id=id)
            if not t:
                raise TimetableException('timetable not found')
            if t.appointments:
                raise TimetableException('timetable have an appointments')

            u = await self.uow.account.get_one(id=data.doctorId)
            if not u:
                raise AccountException('doctor not found')
            if not Roles.DOCTOR in u.roles:
                raise AccountException('user not doctor')

            h = await self.uow.hospital.get_one(id=data.hospitalId)
            if not h:
                raise HospitalException('hospital not found')
            if data.room not in h.rooms:
                raise HospitalException('no room at the hospital')

            from_dt = data.from_dt.replace(tzinfo=None)
            to_dt = data.to_dt.replace(tzinfo=None)

            t = await self.uow.timetable.update(
                id=id,
                **data.model_dump(exclude=['hospitalId', 'doctorId', 'from_dt', 'to_dt']),
                hospital_id=data.hospitalId,
                doctor_id=data.doctorId,
                from_dt=from_dt,
                to_dt=to_dt,
            )
            await self.uow.commit()
            return t.model()

    @uowaccess('timetable')
    async def delete(self, id: int) -> None:
        async with self.uow:
            t = await self.uow.timetable.get_one(id=id)
            if not t:
                raise TimetableException('timetable not found')

            await self.uow.timetable.delete(id)
            await self.uow.commit()
            return None

    @uowaccess('timetable', 'appointment')
    async def create_appointments(
        self, id: int, data: AppointmentsCreate, user_id: int
    ) -> AppoinimentModel:
        async with self.uow:
            t = await self.uow.timetable.get_one(id=id)

            if not t:
                raise TimetableException('timetable not found')

            aware_data_time = data.time.astimezone(timezone.utc)
            aware_from_dt = t.from_dt.astimezone(timezone.utc)
            aware_to_dt = t.to_dt.astimezone(timezone.utc)

            if aware_data_time < aware_from_dt or aware_data_time >= aware_to_dt:
                raise TimetableException('appointment time outside timetable range')

            time_diff = data.time - t.from_dt
            if time_diff.total_seconds() % (30 * 60) != 0:
                raise TimetableException('appointment time must be in 30-minute intervals')

            appointment_exists = await self.uow.appointment.get_one(timetable_id=id, time=data.time)

            if appointment_exists:
                raise TimetableException('time slot already booked')

            a = await self.uow.appointment.add(
                **data.model_dump(), timetable_id=t.id, patient_id=user_id
            )
            await self.uow.commit()
            return a.model()

    @uowaccess('timetable', 'appointment')
    async def get_appointments(self, id: int) -> list[datetime]:
        async with self.uow:
            t = await self.uow.timetable.get_one(id=id)
            if not t:
                raise TimetableException('timetable not found')

            from_time = t.from_dt
            to_time = t.to_dt

            slot_duration = timedelta(minutes=30)
            current_slot = from_time
            available_slots = []

            while current_slot < to_time:
                appointment_exists = await self.uow.appointment.get_one(
                    timetable_id=id, time=current_slot
                )

                if not appointment_exists:
                    available_slots.append(current_slot)

                current_slot += slot_duration

            return available_slots

    @uowaccess('appointment')
    async def get_appointment(self, id: int) -> AppoinimentModel:
        async with self.uow:
            a = await self.uow.appointment.get_one(id=id)
            if not a:
                raise TimetableException('timetable not found')
            return a.model()

    @uowaccess('appointment')
    async def del_appointment(self, id: int) -> None:
        async with self.uow:
            a = await self.uow.appointment.get_one(id=id)
            if not a:
                raise TimetableException('timetable not found')
            await self.uow.appointment.delete(id)
            await self.uow.commit()
            return None

    @uowaccess('timetable')
    async def delete_from_doctor(self, doctor_id: int) -> None:
        async with self.uow:
            t = await self.uow.timetable.get(doctor_id=doctor_id)
            if not t:
                raise TimetableException('doctor`s timetable not found')
            for i in t:
                await self.uow.timetable.delete(i.id)
            await self.uow.commit()
            return None

    @uowaccess('timetable')
    async def delete_from_hospital(self, hospital_id: int) -> None:
        async with self.uow:
            t = await self.uow.timetable.get(hospital_id=hospital_id)
            if not t:
                raise TimetableException('hospital`s timetable not found')
            for i in t:
                await self.uow.timetable.delete(i.id)
            await self.uow.commit()
            return None

    @uowaccess('timetable')
    async def timetable_from_hospital(
        self, hospital_id: int, to: datetime, from_: datetime
    ) -> list[TimetableModel]:
        async with self.uow:
            t = await self.uow.timetable.get_by_time_range(from_, to, hospital_id=hospital_id)
            if not t:
                raise TimetableException('hospital timetable not found for this range')

            return [timetable.model() for timetable in t]

    @uowaccess('timetable')
    async def timetable_from_doctor(
        self, doctor_id: int, to: datetime, from_: datetime
    ) -> list[TimetableModel]:
        async with self.uow:
            t = await self.uow.timetable.get_by_time_range(from_, to, doctor_id=doctor_id)
            if not t:
                raise TimetableException('doctor timetable not found for this range')

            return [timetable.model() for timetable in t]

    @uowaccess('timetable')
    async def timetable_from_room(
        self, hospital_id: int, room: str, to: datetime, from_: datetime
    ) -> list[TimetableModel]:
        async with self.uow:
            t = await self.uow.timetable.get_by_time_range(
                from_, to, hospital_id=hospital_id, room=room
            )
            if not t:
                raise TimetableException('hospital room timetable not found for this range')

            return [timetable.model() for timetable in t]
