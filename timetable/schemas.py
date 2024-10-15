from pydantic import BaseModel
from datetime import datetime


class AvailableAppointments(BaseModel):
    appointments: list[datetime]
