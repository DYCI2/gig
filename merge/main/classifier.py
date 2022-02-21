from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from merge.main.feature import Feature, IntegralFeature, IntegralPitch
from merge.main.label import Label, IntLabel

T = TypeVar('T', bound=Feature)


class Classifier(Generic[T], ABC):

    @abstractmethod
    def classify(self, feature: T) -> Label:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ This function should reset any runtime-related state of the classifier without
            unloading its corpus. If the classifier is stateless, leave this method blank."""
        pass

    def classify_multiple(self, features: List[T]) -> List[Label]:
        """ Function that may be overridden for optimization reasons """
        return [self.classify(feature.value) for feature in features]


class PreTrainable(ABC):
    """ Interface for Classifiers that requires some sort of clustering to be performed without access to any corpus.
        An example of this would be a classifier that loads an external set of data and computers a clustering,
        with or without additional parameters provided by the user"""

    @abstractmethod
    def cluster(self, *args, **kwargs) -> None:
        """ """


class Trainable(ABC):
    """ Interface for Classifiers that requires some sort of clustering to be performed on data from the corpus. """

    @abstractmethod
    def cluster(self, features: List[Feature], *args, **kwargs) -> None:
        """ """


class IdentityClassifier(Classifier[IntegralFeature]):

    def classify(self, feature: IntegralFeature) -> Label:
        return IntLabel(feature.value)

    def clear(self) -> None:
        pass


class PitchClassClassifier(Classifier[IntegralPitch]):

    def classify(self, feature: IntegralPitch) -> Label:
        return IntLabel(feature.value % 12)

    def clear(self) -> None:
        pass
