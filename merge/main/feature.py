from abc import ABC
from typing import TypeVar, Generic

import numpy as np

from merge.main.exceptions import FeatureError

T = TypeVar('T')


class Feature(Generic[T], ABC):
    def __init__(self, value: T):
        self.value: T = value

    # TODO[B6]: Implement way to parse Feature directly from set of onsets etc (without limiting it to onset/duration)
    #  This is one of the most important functions, and it should be able to handle a number of cases, for example
    #  a pre-computed NoteMatrix, pre-computed spectrogram (or compute its own spectrogram), list of onsets, etc.
    #  It should however not take a `Corpus` or a `CorpusEvent`, simply due to the fact that we don't want to add
    #  circular dependencies. If we need a more elaborate strategy for computing a `Feature` from a `CorpusEvent`, we'll
    #  need to add a particular class for this (ex SomeAnalyzer[Feature].__init__(event: CorpusEvent))
    # @classmethod
    # @abstractmethod
    # def from_raw(cls, *args, **kwargs) -> List['Feature']:
    #     """ """


class IntegralFeature(Feature[int], ABC):
    pass


class FloatingFeature(Feature[float], ABC):
    pass


class VectorialFeature(Feature[np.ndarray], ABC):
    """ Feature class for (1d) vectors """

    def __init__(self, value: np.ndarray):
        super().__init__(value)
        if value.ndim > 1:
            raise FeatureError(f"{self.__class__.__name__} only supports one-dimensional vectors")


class FixedVectorialFeature(VectorialFeature, ABC):
    """ Feature class for (1d) vectors with a fixed feature size (for example 12-dimensional chroma, etc.) """

    def __init__(self, value: np.ndarray, size: int):
        super().__init__(value)
        if value.size != size:
            raise FeatureError(f"{self.__class__.__name__} can only handle vectors of size {size}. "
                               f"Actual size was {value.size}")


class IntegralPitch(IntegralFeature, ABC):
    pass


class TopNote(IntegralPitch):
    pass

    # TODO
    # @classmethod
    # def from_raw(cls, *args, **kwargs) -> List['Feature']:
    #   """ """


class Chroma12(FixedVectorialFeature, ABC):
    """ Base class for 12-dimensional chroma-based features """

    def __init__(self, value: np.ndarray):
        super().__init__(value=value, size=12)


class OnsetChroma(Chroma12):
    pass

    # TODO
    # @classmethod
    # def from_raw(cls, *args, **kwargs) -> List['Feature']:
    #   """ """


class MeanChroma(Chroma12):
    pass

    # TODO
    # @classmethod
    # def from_raw(cls, *args, **kwargs) -> List['Feature']:
    #     """ """
