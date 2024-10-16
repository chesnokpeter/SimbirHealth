from core.exceptions import BaseExceptions

from pydantic import BaseModel

class JWTExceptions(BaseExceptions): ...


class JWTAccessExceptions(JWTExceptions): ...


class JWTRefreshExceptions(JWTExceptions): ...


class ErrorModel(BaseModel):
    error: str