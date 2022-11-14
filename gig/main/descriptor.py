from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, List

import numpy as np

from gig.io.parsable import Parsable
from gig.main.exceptions import DescriptorError

T = TypeVar('T')


class Descriptor(Generic[T], Parsable['Descriptor'], ABC):
    def __init__(self, value: T):
        self.value: T = value

    # TODO: Implement way to parse Descriptor directly from set of onsets etc (without limiting it to onset/duration)
    #  This is one of the most important functions, and it should be able to handle a number of cases, for example
    #  a pre-computed NoteMatrix, pre-computed spectrogram (or compute its own spectrogram), list of onsets, etc.
    #  It should however not take a `Corpus` or a `CorpusEvent`, simply due to the fact that we don't want to add
    #  circular dependencies. If we need a more elaborate strategy for computing a `Feature` from a `CorpusEvent`, we'll
    #  need to add a particular class for this (ex SomeAnalyzer[Feature].__init__(event: CorpusEvent))
    # TODO
    #  one good solution would perhaps be to simply add interfaces for compatibility, e.g. AudioDescriptor and
    #  MidiDescriptor, defined simply as AudioDescriptor: @abstractmethod def analyze_audio(...) and MidiDescriptor:
    #  @abstracmethod def analyze_midi(...). This would allow more flexibility, e.g.
    #  PitchDescriptor(Descriptor, MidiDescriptor, AudioDescriptor).
    #  (i.e. that neither MidiDescriptor or AudioDescriptor inherits from Descriptor, but are rather pure interfaces).
    # TODO
    #  But perhaps this is too inflexible. A third solution would be to separate out `method of analysis` from
    #  the data itself, so that we could for example use multiple strategies to analyze pitch into the same class.
    #  (for example if we want both Yin and MelodicSalience to return pitch). The problem with this strategy is that
    #  we might want both of them in the corpus + some custom data parsed from mubu, all three stored under pitch.
    #  What do we do then?
    # @classmethod
    # @abstractmethod
    # def from_raw(cls, *args, **kwargs) -> List['Feature']:
    #     """ """

    @staticmethod
    @abstractmethod
    def _compatible_descriptors() -> List[Type['Descriptor']]:
        """ In most cases, classification / influence will only work for descriptors of the same type. If
            there however are other descriptor types that describe the same domain and should be compatible each other,
            these may be specified here. It's also possible to simply specify a given base class as compatible.

            For example: assuming that we have TopNote(MidiPitch) and BassNote(MidiPitch) describing the same domain
            (MIDI pitches in range 21-108), if we define `_compatible_descriptors` as `[MidiPitch]` for both of them,
            it will be possible to influence a classifier trained on either `TopNote` values or `BassNote` values
            with influences of any MidiPitch. If not specified, only `TopNote` values will work for a classifier trained
            on `TopNote` values.
        """
        return []

    @classmethod
    def compatible_with(cls, descriptor_type: Type['Descriptor']) -> bool:
        """ Note: this is not symmetric,
            descriptor1.compatible_with(descriptor2) and descriptor2.compatible_with(descriptor1)
            may return different results. Effectively, this is just an extension of the `issubclass` method,
            where we want to add some degree of symmetry for runtime parsing reasons.

            For example, given the relation TopNote `is a` MidiPitch, `issubclass(MidiPitch, TopNote)` is false.
            What this function does is effectively adding some degree of symmetry by defining `_compatible_descriptors`.
            If we in this case define `_compatible_descriptors = [MidiPitch]`,
            `TopNote.compatible_with(MidiPitch)` now returns true (while `issubclass(MidiPitch, TopNote)` is false).

            In context, the usage would be
                `descriptor_that_the_prospector_has_been_trained_on.compatible_with(type(influence_descriptor))`

            """
        return issubclass(descriptor_type, cls) or descriptor_type in cls._compatible_descriptors()


class IntegralDescriptor(Descriptor[int], ABC):
    pass


class FloatingDescriptor(Descriptor[float], ABC):
    pass


class VectorialDescriptor(Descriptor[np.ndarray], ABC):
    """ Feature class for (1d) vectors """

    def __init__(self, value: np.ndarray):
        super().__init__(value)
        if value.ndim > 1:
            raise DescriptorError(f"{self.__class__.__name__} only supports one-dimensional vectors")


class FixedVectorialFeature(VectorialDescriptor, ABC):
    """ Feature class for (1d) vectors with a fixed feature size (for example 12-dimensional chroma, etc.) """

    def __init__(self, value: np.ndarray, size: int):
        super().__init__(value)
        if value.size != size:
            raise DescriptorError(f"{self.__class__.__name__} can only handle vectors of size {size}. "
                               f"Actual size was {value.size}")


class MidiPitch(IntegralDescriptor):
    @staticmethod
    def _compatible_descriptors() -> List[Type['Descriptor']]:
        return super()._compatible_descriptors()


class Chroma12(FixedVectorialFeature):
    """ Base class for 12-dimensional chroma-based descriptors.
        Stored as a numpy array with shape (12,)
    """
    SIZE = 12

    def __init__(self, value: np.ndarray):
        if value.size != self.SIZE:
            raise DescriptorError(f"{self.__class__.__name__} can only handle values of "
                                  f"size {self.SIZE} (actual: {value.size})")

        super().__init__(value=value.reshape(-1), size=value.size)

    @staticmethod
    def _compatible_descriptors() -> List[Type['Descriptor']]:
        return super()._compatible_descriptors()
