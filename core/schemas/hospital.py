from pydantic import BaseModel



class CreateHospital(BaseModel):
    name: str
    adress: str
    contactPhone: str
    rooms: list[str]
