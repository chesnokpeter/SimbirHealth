from core.exceptions import CoreException


class JWTExceptions(CoreException):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)



class JWTAccessExceptions(JWTExceptions): ...


class JWTRefreshExceptions(JWTExceptions): ...
