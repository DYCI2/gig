from abc import ABC
from typing import TypeVar, Generic

from merge.main.corpus_event import CorpusEvent
from merge.main.feature import Feature
from merge.main.label import Label

T = TypeVar('T')


class Influence(Generic[T], ABC):
    def __init__(self, influence: T):
        self.value: T = influence


class CorpusInfluence(Influence[CorpusEvent]):
    pass


class FeatureInfluence(Influence[Feature]):
    pass


class LabelInfluence(Influence[Label]):
    pass


class TriggerInfluence(Influence[None]):
    pass
