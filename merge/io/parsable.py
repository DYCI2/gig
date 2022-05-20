from abc import ABC
from typing import TypeVar, Generic, Type

from merge.io.introspective import Introspective
from merge.main.exceptions import InputError

T = TypeVar('T')


class Parsable(Generic[T], ABC):
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
