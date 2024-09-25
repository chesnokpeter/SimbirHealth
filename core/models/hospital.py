from pydantic import BaseModel

from core.models.abstract import DbAbsModel


class HospitalModel(BaseModel, DbAbsModel):
    id: int

    name: str
    adress: str
    contactPhone: str
    rooms: str
