class CoreException(Exception):
    error = 'Base Core Error'

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class UOWException(CoreException): ...


class NoConnectorForRepo(UOWException): ...


class NoAccessForRepo(UOWException): ...


class AccountException(CoreException):
    error = 'User Error'



class RestExceptions(CoreException): ...


