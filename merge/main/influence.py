from abc import ABC
from typing import TypeVar, Generic

from merge.main.corpus_event import CorpusEvent
from merge.main.feature import Feature
from merge.main.label import Label

T = TypeVar('T')


class Influence(Generic[T], ABC):
    def __init__(self, value: T):
        self.value = value


class NoInfluence(Influence[None]):
    """ Class to trigger incrementation of state without any external requirements to match """

    def __init__(self, value: None = None):
        super().__init__(value=value)


class CorpusInfluence(Influence[CorpusEvent]):
    """ Class to trigger incrementation of state based on a `CorpusEvent` """
    pass


class FeatureInfluence(Influence[Feature]):
    """ Class to trigger incrementation of state based on a `Feature` """
    pass


class LabelInfluence(Influence[Label]):
    """ Class to trigger incrementation of state based on a `Label` """
    pass
