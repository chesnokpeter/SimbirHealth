from pydantic import BaseModel
from core.enums import Roles

from core.models.abstract import DbAbsModel


class AccountModel(BaseModel, DbAbsModel):
    id: int

    lastName: str
    firstName: str
    username: str
    password: str
    roles: list[Roles]
