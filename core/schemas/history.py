from pydantic import BaseModel, Field
from datetime import datetime


class CreateHistory(BaseModel):
    date: datetime
    pacientId: int = Field(gt=0)
    hospitalId: int = Field(gt=0)
    doctorId: int = Field(gt=0)

    room: str
    data: str
