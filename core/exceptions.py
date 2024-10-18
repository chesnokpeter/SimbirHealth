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


class ServiceException(CoreException): 
    error = 'Service Error'





class AccountException(ServiceException): ...


class HospitalException(ServiceException): ...


class TimetableException(ServiceException): ...


class DocumentException(ServiceException): ...




class NotFoundError(ServiceException):
    error = 'Not Found Error'

class ConflictError(ServiceException):
    error = 'Conflict Error'

class IncorrectError(ServiceException):
    error = 'Incorrect Error'

class PermissionError(ServiceException):
    error = 'Permission Error'