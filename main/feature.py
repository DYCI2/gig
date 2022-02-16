from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

T = TypeVar('T')


class Feature(Generic[T], ABC):
    def __init__(self, value: T):
        self.value: T = value

    @classmethod
    @abstractmethod
    def from_raw(cls, *args, **kwargs) -> List['Feature']:
        """ """
