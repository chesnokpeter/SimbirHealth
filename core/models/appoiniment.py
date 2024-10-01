from pydantic import BaseModel
from datetime import datetime
from core.models.abstract import DbAbsModel

class AppoinimentModel(BaseModel, DbAbsModel):
    id: int
    timetable_id: int
    time: datetime
    


