class CoreException(Exception):
    error = 'Base Core Error'

    def __init__(self, desc: str, *args: object) -> None:
        super().__init__(*args)
        self.desc = desc


class UOWException(CoreException): ...


class NoConnectorForRepo(UOWException): ...


class NoAccessForRepo(UOWException): ...


class AccountException(CoreException):
    error = 'User Error'



class RestExceptions(CoreException): ...


class JWTExceptions(RestExceptions):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class JWTAccessExceptions(JWTExceptions): ...


class JWTRefreshExceptions(JWTExceptions): ...
