from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime, timedelta

class TimetableCreate(BaseModel):
    hospitalId: int = Field(gt=0)
    doctorId: int = Field(gt=0)
    from_dt: datetime = Field(alias='from')
    to_dt: datetime = Field(alias='to')
    room: str
    

    @field_validator('from_dt', 'to_dt')
    def validate_time_format(cls, value: datetime):
        if value.minute % 30 != 0 or value.second != 0 or value.microsecond != 0:
            raise ValueError("время должно быть кратно 30 минутам, секунды и миллисекунды должны быть равны 0")
        return value

    @field_validator('to_dt')
    def validate_time_difference(cls, to_dt: datetime, values: dict):
        from_dt = values.get('from_dt')
        if from_dt and to_dt <= from_dt:
            raise ValueError('"to" должно быть больше "from"')
        
        if from_dt and (to_dt - from_dt) > timedelta(hours=12):
            raise ValueError('разница между "to" и "from" не должна превышать 12 часов')
        return to_dt

    class Config:
        schema_extra = {
            "example": {
                "hospitalId": 1,
                "doctorId": 123,
                "from_dt": "2024-04-25T11:30:00Z",
                "to_dt": "2024-04-25T12:00:00Z",
                "room": "101"
            }
        }