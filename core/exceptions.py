class CoreException(Exception):
    error = 'Base Core Error'

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class UOWException(CoreException):
    error = 'UOW Error'


class NoConnectorForRepo(UOWException):
    error = 'No Connector For Repo'


class NoAccessForRepo(UOWException):
    error = 'No Access For Repo'


class BaseExceptions(CoreException): 
    error = 'Base Error'





class AccountException(BaseExceptions): ...


class HospitalException(BaseExceptions): ...


class TimetableException(BaseExceptions): ...


class DocumentException(BaseExceptions): ...




class NotFoundError(BaseException):
    error = 'Not Found Error'

class ConflictError(BaseException):
    error = 'Already Error'

class IncorrectError(BaseException):
    error = 'Incorrect Error'

