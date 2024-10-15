from pydantic import BaseModel

from core.models.abstract import DbAbsModel


class LostokenModel(BaseModel, DbAbsModel):
    id: int

    accessToken: str
    refreshToken: str
