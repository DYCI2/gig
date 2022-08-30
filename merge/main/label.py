from abc import ABC
from typing import TypeVar, Generic, List

T = TypeVar('T')


class Label(Generic[T], ABC):
    def __init__(self, label: T):
        self.label: T = label

    pass  # TODO: Empty interface for now


class IntLabel(Label[int]):

    def __repr__(self):
        return f"{self.__class__.__name__}(label={self.label})"


class ListLabel(Label[List[T]]):
    pass  # TODO: DYCI2 implementation


class ChordLabel(Label):
    pass  # TODO: DYCI2 implementation
