from pydantic import BaseModel, field_validator




class CreateHospital(BaseModel):
    name: str
    adress: str
    contactPhone: str
    rooms: list[str]

    @field_validator('contactPhone')
    def validate_phone(cls, value: str):
        if not (value.startswith('+') and len(value) == 12 and value[1:].isdigit()):
            raise ValueError('Некорректный номер телефона')
        return value
    
    class Config:
        json_schema_extra = {
            'example': {
                'name': 'горбольница',
                'adress': 'ул. Пушкина д. Колотушкина',
                'contactPhone': '+79103264051',
                'rooms': ['главврач']
            }
        }