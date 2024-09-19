from abc import ABC, abstractmethod


class AbsService(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError
