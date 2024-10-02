from abc import ABC, abstractmethod
from typing import Annotated, TypeAlias
from core.uow import UnitOfWork, BaseUnitOfWork

UnitOfWork: TypeAlias = Annotated[BaseUnitOfWork, UnitOfWork]


class AbsService(ABC):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
