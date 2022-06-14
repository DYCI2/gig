from abc import ABC, abstractmethod
from typing import List, Optional

from merge.io.parsable import Parsable
from merge.main.descriptor import Descriptor, IntegralDescriptor, MidiPitch
from merge.main.exceptions import ClassificationError
from merge.main.label import Label, IntLabel


class Classifier(Parsable['Classifier'], ABC):

    @abstractmethod
    def classify(self, descriptor: Descriptor) -> Label:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ This function should reset any runtime-related state of the classifier without
            unloading its corpus. If the classifier is stateless, leave this method blank."""
        pass

    def classify_multiple(self, descriptors: List[Descriptor]) -> List[Label]:
        """ Function that may be overridden for optimization reasons """
        return [self.classify(descriptor) for descriptor in descriptors]


class Trainable(ABC):
    """ Interface for Classifiers that requires some sort of clustering to be performed on data from the corpus. """

    @abstractmethod
    def cluster(self, descriptors: Optional[List[Descriptor]] = None, *args, **kwargs) -> None:
        """ """


class IdentityClassifier(Classifier):

    def classify(self, descriptor: Descriptor) -> Label:
        if not IntegralDescriptor:
            raise ClassificationError(f"{self.__class__.__name__} can only handle integral values")

        return IntLabel(descriptor.value)

    def clear(self) -> None:
        pass


class PitchClassClassifier(Classifier):

    def classify(self, descriptor: Descriptor) -> Label:
        if not isinstance(descriptor, MidiPitch):
            raise ClassificationError(f"{self.__class__.__name__} can only handle integral pitch descriptors")

        return IntLabel(descriptor.value % 12)

    def clear(self) -> None:
        pass
