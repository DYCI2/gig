from abc import ABC, abstractmethod
from typing import List

from main.feature import Feature
from main.label import Label


class Classifier(ABC):

    @abstractmethod
    def classify(self, feature: Feature) -> Label:
        """ """

    @abstractmethod
    def classify_multiple(self, features: List[Feature]) -> List[Label]:
        """ """


class PreTrainedClassifier(Classifier, ABC):
    @abstractmethod
    def cluster(self, **kwargs) -> None:
        """ """


class TrainableClassifier(Classifier, ABC):
    @abstractmethod
    def cluster(self, features: List[Feature], **kwargs) -> None:
        """ """
