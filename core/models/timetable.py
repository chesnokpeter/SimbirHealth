from pydantic import BaseModel
from datetime import datetime
from core.models.abstract import DbAbsModel


class TimetableModel(BaseModel, DbAbsModel):
    id: int
    hospital_id: int
    doctor_id: int
    from_time: datetime
    to_time: datetime
    room: str
    appointments: list

