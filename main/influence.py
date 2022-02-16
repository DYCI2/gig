from typing import TypeVar, Generic

from main.corpus_event import CorpusEvent
from main.feature import Feature
from main.label import Label

T = TypeVar('T')


class Influence(Generic[T]):
    def __init__(self, influence: T):
        self.influence: T = influence


class CorpusInfluence(Influence[CorpusEvent]):
    pass


class FeatureInfluence(Influence[Feature]):
    pass


class LabelInfluence(Influence[Label]):
    pass


class TriggerInfluence(Influence[None]):
    pass
