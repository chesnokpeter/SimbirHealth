from typing import Any, Generic, Type, TypeAlias, TypeVar
from functools import wraps
from core.models.abstract import AbsModel, DbAbsModel, RestAPIAbsModel

AbsSession: TypeAlias = Any

TSESSION = TypeVar('TSESSION', bound=AbsSession)


class AbsRepo(Generic[TSESSION]):
    model: AbsModel
    reponame: str

    def __init__(self, require_connector: str):
        self.require_connector = require_connector

    def __call__(self, session: TSESSION) -> AbsModel:
        self.session = session


class DbAbsRepo(AbsRepo[TSESSION]):
    model: DbAbsModel

    async def get(self):
        raise NotImplementedError

    async def get_one(self):
        raise NotImplementedError

    async def add(self):
        raise NotImplementedError

    async def offset(self):
        raise NotImplementedError

    async def update(self):
        raise NotImplementedError

    async def delete(self):
        raise NotImplementedError


class RestAPIAbsRepo(AbsRepo[TSESSION]):
    model: RestAPIAbsModel

    async def get_one(self):
        raise NotImplementedError


def repo_logger(cls) -> 'cls':
    class Logger:
        def __init__(self, *args, **kwargs):
            self.wrapped = cls(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            return self.wrapped(*args, **kwargs)

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
                    except Exception as e:
                        print(f"ERROR:     {cls.__name__}.{name}{pre} - {e.with_traceback}")
                        raise e
                return decorator
            return attr

    return Logger