from abc import ABC, abstractmethod
from typing import Union

from merge.main.feature import Feature
from merge.main.label import Label


class Transform(ABC):

    @classmethod
    @abstractmethod
    def from_id(cls, transform_id: int) -> 'Transform':
        """ """

    @abstractmethod
    def apply(self, obj: Union[Label, Feature]) -> Union[Label, Feature]:
        """ """

    @abstractmethod
    def inverse(self, obj: Union[Label, Feature]) -> Union[Label, Feature]:
        """ """

    @abstractmethod
    def to_id(self) -> int:
        """ """
