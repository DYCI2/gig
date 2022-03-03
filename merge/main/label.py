from abc import ABC
from typing import TypeVar, Generic, List

T = TypeVar('T')


class Label(Generic[T], ABC):
    def __init__(self, value: T):
        self.value: T = value

    pass  # TODO: Empty interface for now


class IntLabel(Label[int]):

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"


class ListLabel(Label[List[T]]):
    pass  # TODO: DYCI2 implementation


class ChordLabel(Label):
    pass  # TODO: DYCI2 implementation
