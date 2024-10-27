from abc import ABC
from typing import Annotated, TypeAlias
from core.uow import UnitOfWork, AllReposUnitOfWork
from functools import wraps
from core.exceptions import ServiceException


UnitOfWork: TypeAlias = Annotated[AllReposUnitOfWork, UnitOfWork]


class AbsService(ABC):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow



def service_logger(cls) -> 'cls':
    class Logger:
        def __init__(self, *args, **kwargs):
            self.wrapped = cls(*args, **kwargs)

        def __getattr__(self, name):
            attr = getattr(self.wrapped, name)
            if callable(attr):
                @wraps(attr)
                async def decorator(*args, **kwargs):
                    pre_args = ' '.join(map(str, args))
                    pre_kwargs = ' '.join(f'{k}={v}' for k, v in kwargs.items())
                    pre = f"({pre_args}, {pre_kwargs})"
                    try:
                        result = await attr(*args, **kwargs)
                        print(f"INFO:     {cls.__name__}.{name}{pre} - {result}")
                        return result
                    except ServiceException as e:
                        print(f"WARN:     {cls.__name__}.{name}{pre} - {e.error}")
                        raise e
                return decorator
            return attr

    return Logger