from pydantic import BaseModel, Field
from core.models.account import AccountModel


class AccessSch(BaseModel):
    accessToken: str


class AccessRefreshSch(AccessSch):
    refreshToken: str


class AccountModelWithoutPassword(AccountModel):
    # password: str = Field(exclude=True)
    ...