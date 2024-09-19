from pydantic import BaseModel
from core.enums import Roles

class AccountModel(BaseModel):
    id: int

    lastName: str
    firstName: str
    username: str
    password: str
    roles: list[Roles]
