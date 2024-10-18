from core.exceptions import ServiceException

from pydantic import BaseModel

class JWTExceptions(ServiceException): ...


class JWTAccessExceptions(JWTExceptions): ...


class JWTRefreshExceptions(JWTExceptions): ...


class ErrorModel(BaseModel):
    error: str