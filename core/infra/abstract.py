from abc import ABC, abstractmethod


class DbAbsTable:
    id: int

    @abstractmethod
    def model(self):
        raise NotImplementedError


class AbsConnector(ABC):
    _session = None
    connector_name = None

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def session(self):
        raise NotImplementedError
