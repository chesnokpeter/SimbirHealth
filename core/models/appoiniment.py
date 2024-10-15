from pydantic import BaseModel
from datetime import datetime
from core.models.abstract import DbAbsModel


class AppoinimentModel(BaseModel, DbAbsModel):
    id: int
    time: datetime
    timetable_id: int
    patient_id: int
