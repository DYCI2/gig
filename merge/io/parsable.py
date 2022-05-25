from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic, Type

from merge.io.introspective import Introspective
from merge.main.exceptions import InputError

T = TypeVar('T')


class Parsable(Generic[T]):
    @classmethod
    def from_string(cls, class_name: str, include_abstract: bool = False) -> Type[T]:
        """ Returns a subclass of the given class corresponding to the given name (case-insensitive)
            Override this method for more complex parsing.
            raises: InputError if no class with the provided name exists
        """
        try:
            return Introspective.introspect(cls, include_abstract=include_abstract)[class_name.lower()]
        except KeyError:
            raise InputError(f"No class named '{class_name}' exists in '{cls.__name__}'")


class ParsableWithDefault(Parsable[T], ABC):
    """ Similar to `Parsable` but returns a type defined in `default()` if no value is provided (empty string)"""

    @classmethod
    def from_string(cls, class_name: str, include_abstract: bool = False) -> Type[T]:
        if not class_name:
            return cls.default()
        else:
            return super().from_string(class_name, include_abstract)

    @classmethod
    @abstractmethod
    def default(cls) -> Type[T]:
        """ Returns default type for given class. """


class ParsableEnum(Enum):
    @classmethod
    def from_string(cls, name: str, enforce_lowercase_strings: bool = True) -> Enum:
        """ raises: InputError if key is not found. Implemented for consistency with `Parsable`"""
        try:
            if enforce_lowercase_strings:
                return cls(name.lower())
            else:
                return cls(name)

        except ValueError as e:
            raise InputError(e) from e
