from pydantic import BaseModel

class AccessSch(BaseModel):
    accessToken: str

class AccessRefreshSch(AccessSch):
    refreshToken: str