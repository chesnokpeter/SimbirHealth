from abc import ABC, abstractmethod
from typing import Any, TypeAlias

AbsModel: TypeAlias = Any


class DbAbsModel(ABC):
    id: int

    @abstractmethod
    def model_dump(self):
        raise NotImplementedError

class RestAPIAbsModel(ABC):
    ...
