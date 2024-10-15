from pydantic import BaseModel
from core.enums import Roles


class SignUpSch(BaseModel):
    lastName: str
    firstName: str
    username: str
    password: str


class AdminCreate(SignUpSch):
    roles: list[Roles]


class SignInSch(BaseModel):
    username: str
    password: str


class SignOutSch(BaseModel):
    accessToken: str
    refreshToken: str


class UpdateSch(BaseModel):
    lastName: str
    firstName: str
    password: str
