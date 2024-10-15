from pydantic import BaseModel
from datetime import datetime


class CreateHistory(BaseModel):
    date: datetime
    pacientId: int
    hospitalId: int
    doctorId: int

    room: str
    data: str
