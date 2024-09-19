from pydantic import BaseModel


class SignUpSch(BaseModel):
    lastName: str
    firstName: str
    username: str
    password: str