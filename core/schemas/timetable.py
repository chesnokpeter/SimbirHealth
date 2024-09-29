from pydantic import BaseModel, conint, validator
from datetime import datetime, timedelta
from typing import Any

class TimetableEntry(BaseModel):
    hospitalId = conint(gt=0)  # Ensure hospitalId is a positive integer
    doctorId = conint(gt=0)    # Ensure doctorId is a positive integer
    from_: datetime           # Using from_ to avoid conflict with Python's keyword
    to: datetime
    room: str

    @validator('from_', 'to')
    def check_datetime_format(cls, value: datetime) -> datetime:
        if value.second != 0:
            raise ValueError("Seconds must be zero in the datetime")
        if value.minute % 30 != 0:
            raise ValueError("Minutes must be a multiple of 30")
        return value

    @validator('to')
    def check_duration(cls, to_value: datetime, values: dict[str, Any]) -> datetime:
        from_value = values.get('from_')
        if from_value is not None:
            if to_value <= from_value:
                raise ValueError("'to' must be greater than 'from'")
            if to_value - from_value > timedelta(hours=12):
                raise ValueError("Difference between 'to' and 'from' must not exceed 12 hours")
        return to_value

# Example Usage
try:
    entry = TimetableEntry(
        hospitalId=1,
        doctorId=123,
        from_="2024-04-25T11:30:00Z",
        to="2024-04-25T12:00:00Z",
        room="Room 101"
    )
    print(entry)
except ValueError as e:
    print(e)