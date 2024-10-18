from core.exceptions import ServiceException

from pydantic import BaseModel

class JWTExceptions(ServiceException): ...


class ErrorModel(BaseModel):
    error: str

