from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterable, Optional, Any

import numpy as np

from merge.main.exceptions import ConfigurationError

T = TypeVar('T')


class ParameterRange(Generic[T], ABC):
    @abstractmethod
    def __contains__(self, item: T) -> bool:
        """ TODO: Docstring """

    @abstractmethod
    def renderer_info(self) -> str:
        """ TODO: Docstring """


class NominalRange(ParameterRange):
    def __init__(self, labels: Iterable[T]):
        self.labels: Iterable[T] = labels

    def __contains__(self, item):
        return item in self.labels

    def renderer_info(self) -> str:
        return " ".join(self.labels)


class NumericRange(ParameterRange):
    def __init__(self, lower_bound: Optional[T] = None, upper_bound: Optional[T] = None):
        self.lower_bound: Optional[T] = lower_bound
        self.upper_bound: Optional[T] = upper_bound

    def __contains__(self, item: T) -> bool:
        if self.lower_bound is not None and item < self.lower_bound:
            return False
        if self.upper_bound is not None and item > self.upper_bound:
            return False
        return True

    def renderer_info(self) -> str:
        return str(self.lower_bound) + " " + str(self.upper_bound)


class MaxType:
    @abstractmethod
    def matches(self, value: Any):
        """ TODO: Docstring
            raises: ConfigurationError if parameter cannot be compared
        """

    @abstractmethod
    def renderer_info(self) -> str:
        """ """


class MaxInt(MaxType):
    def matches(self, value: Any):
        return isinstance(value, int)

    def renderer_info(self) -> str:
        return "int"


class MaxFloat(MaxType):
    def matches(self, value: Any):
        return isinstance(value, float)

    def renderer_info(self) -> str:
        return "float"


class MaxString(MaxType):
    def matches(self, value: Any):
        return isinstance(value, str)

    def renderer_info(self) -> str:
        return "str"


class MaxBool(MaxType):
    @staticmethod
    def range() -> ParameterRange:
        return NumericRange(0, 1)

    def matches(self, value: Any):
        return isinstance(value, bool)

    def renderer_info(self) -> str:
        return "bool"


class MaxList(MaxType):
    def matches(self, value: Any):
        return isinstance(value, (list, np.ndarray))

    def renderer_info(self) -> str:
        return "list"


class MaxListSized(MaxType):
    def __init__(self, size: int):
        self.size = size

    def matches(self, value: Any):
        return isinstance(value, (list, np.ndarray)) and len(value) == self.size

    def renderer_info(self) -> str:
        return f"list[{self.size}]"


class MaxCustom(MaxType):
    def __init__(self, type_info: str):
        self.type_info = type_info

    def matches(self, value: Any):
        raise ConfigurationError(f"A parameter of type {self.__class__.__name__} cannot be compared")

    def renderer_info(self) -> str:
        return self.type_info
