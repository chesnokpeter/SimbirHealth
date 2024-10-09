from abc import ABC, abstractmethod
from typing import Annotated, TypeAlias
from core.uow import UnitOfWork, AllReposUnitOfWork

UnitOfWork: TypeAlias = Annotated[AllReposUnitOfWork, UnitOfWork]


class AbsService(ABC):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
