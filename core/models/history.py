from pydantic import BaseModel
from datetime import datetime
from core.models.abstract import DbAbsModel

class HistoryModel(BaseModel, DbAbsModel):
    id: int 
    date: datetime
    pacientId: int
    hospitalId: int
    doctorId: int

    room: str
    data: str

