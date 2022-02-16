from abc import ABC, abstractmethod
from typing import Union

from main.feature import Feature
from main.label import Label


class Transform(ABC):

    @abstractmethod
    def apply(self, data: Union[Label, Feature]) -> Union[Label, Feature]:
        """ """

    @abstractmethod
    def inverse(self, data: Union[Label, Feature]) -> Union[Label, Feature]:
        """ """
