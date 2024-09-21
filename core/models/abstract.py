from abc import ABC, abstractmethod
from typing import Any, TypeAlias

AbsModel: TypeAlias = Any


class DbAbsModel(ABC):
    id: int

    @abstractmethod
    def model_dump(self):
        raise NotImplementedError

class MemoryAbsModel(ABC):
    memory_model_name: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.memory_model_name = cls.__name__

    @abstractmethod
    def model_dump(self):
        raise NotImplementedError
