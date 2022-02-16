from abc import ABC
from typing import TypeVar, Generic

T = TypeVar('T')


class Feature(Generic[T], ABC):
    def __init__(self, value: T):
        self.value: T = value

    # TODO[B6]: Implemnet way to parse Feature directly from set of onsets etc (without limiting it to onset/duration)
    # @classmethod
    # @abstractmethod
    # def from_raw(cls, *args, **kwargs) -> List['Feature']:
    #     """ """
