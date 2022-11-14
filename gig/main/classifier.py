from abc import ABC, abstractmethod
from typing import List, Optional, Type

from gig.io.parsable import Parsable
from gig.main.descriptor import Descriptor, IntegralDescriptor, MidiPitch
from gig.main.exceptions import ClassificationError
from gig.main.label import Label, IntLabel


class Classifier(Parsable['Classifier'], ABC):

    @abstractmethod
    def classify(self, descriptor: Descriptor) -> Label:
        """ raises: ClassificationError if classification fails """

    @abstractmethod
    def clear(self) -> None:
        """ This function should reset any runtime-related state of the classifier without
            unloading its corpus. If the classifier is stateless, leave this method blank."""
        pass

    @abstractmethod
    def compatible_with(self, descriptor_type: Type[Descriptor]) -> bool:
        """ This function may be used to specify descriptor type bounds for the classifier. If the classifier raises
            `ClassificationError` on calling `classify` with certain descriptors, it is recommended to specify the
            boundary explicitly in this function in order to allow static evaluation of a given user configuration.
        """

    def classify_multiple(self, descriptors: List[Descriptor]) -> List[Label]:
        """ Function that may be overridden for optimization reasons
            raises: ClassificationError if classification of one or more descriptors fails """
        return [self.classify(descriptor) for descriptor in descriptors]


class Trainable(ABC):
    """ Interface for Classifiers that requires some sort of pre-processing / clustering to be
        performed on data from the corpus. """

    @abstractmethod
    def pre_process(self, descriptors: Optional[List[Descriptor]] = None, *args, **kwargs) -> None:
        """ raises: ClassificationError if pre-processing fails """


class IdentityClassifier(Classifier):

    def classify(self, descriptor: Descriptor) -> Label:
        if not IntegralDescriptor:
            raise ClassificationError(f"{self.__class__.__name__} can only handle integral values")

        return IntLabel(descriptor.value)

    def clear(self) -> None:
        pass

    def compatible_with(self, descriptor_type: Type[Descriptor]) -> bool:
        return issubclass(descriptor_type, IntegralDescriptor)


class PitchClassClassifier(Classifier):

    def classify(self, descriptor: Descriptor) -> Label:
        if not isinstance(descriptor, MidiPitch):
            raise ClassificationError(f"{self.__class__.__name__} can only handle integral pitch descriptors")

        return IntLabel(descriptor.value % 12)

    def clear(self) -> None:
        pass

    def compatible_with(self, descriptor_type: Type[Descriptor]) -> bool:
        return issubclass(descriptor_type, MidiPitch)
