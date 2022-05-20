from abc import ABC, abstractmethod
from typing import Union

from merge.main.descriptor import Descriptor
from merge.main.label import Label


class Transform(ABC):

    @classmethod
    @abstractmethod
    def from_id(cls, transform_id: int) -> 'Transform':
        """ """

    @abstractmethod
    def apply(self, obj: Union[Label, Descriptor]) -> Union[Label, Descriptor]:
        """ """

    @abstractmethod
    def inverse(self, obj: Union[Label, Descriptor]) -> Union[Label, Descriptor]:
        """ """

    @abstractmethod
    def to_id(self) -> int:
        """ """
