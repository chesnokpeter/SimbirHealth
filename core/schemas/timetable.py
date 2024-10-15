from pydantic import BaseModel, Field, field_validator, ValidationInfo
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
            raise ValueError(
                'время должно быть кратно 30 минутам, секунды и миллисекунды должны быть равны 0'
            )
        return value

    @field_validator('to_dt')
    def validate_time_difference(cls, to_dt: datetime, values: ValidationInfo):
        from_dt = values.data['from_dt']
        if to_dt <= from_dt:
            raise ValueError('"to" должно быть больше "from"')

        if (to_dt - from_dt) > timedelta(hours=12):
            raise ValueError('разница между "to" и "from" не должна превышать 12 часов')
        return to_dt

    class Config:
        json_schema_extra = {
            'example': {
                'hospitalId': 1,
                'doctorId': 1,
                'from': '2024-04-25T11:30:00Z',
                'to': '2024-04-25T12:00:00Z',
                'room': '1',
            }
        }


class AppointmentsCreate(BaseModel):
    time: datetime
