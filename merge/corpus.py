from abc import ABC, abstractmethod
from typing import List, Type, Optional

from merge.main.corpus_event import CorpusEvent
from merge.main.feature import Feature


class Corpus(ABC):
    def __init__(self, events: List[CorpusEvent], feature_types: Optional[List[Type[Feature]]] = None):
        # TODO[B4]: handle feature types (if not provided, gather all from events. Also: pre-compute feature values
        self.events: List[CorpusEvent] = events

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> 'Corpus':
        """ """

    @classmethod
    @abstractmethod
    def from_file(cls, filepath: str, **kwargs) -> 'Corpus':
        """ """

    @abstractmethod
    def export(self, filepath: str, **kwargs) -> None:
        """ """


class FreeCorpus(Corpus):
    pass


class AudioCorpus(Corpus):
    pass


class MidiCorpus(Corpus):
    pass
