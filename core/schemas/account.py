from pydantic import BaseModel


class SignUpSch(BaseModel):
    lastName: str
    firstName: str
    username: str
    password: str

class SignIn(BaseModel):
    username: str
    password: str

class SignOut(BaseModel):
    accessToken: str
    refreshToken: str