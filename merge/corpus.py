import logging
from abc import ABC, abstractmethod
from typing import List, Type, Optional, TypeVar, Generic

from merge.main.corpus_event import CorpusEvent
from merge.main.exceptions import CorpusError
from merge.main.feature import Feature
from merge.main.label import Label

E = TypeVar('E', bound=CorpusEvent)


class Corpus(Generic[E], ABC):
    def __init__(self, events: List[E],
                 feature_types: Optional[List[Type[Feature]]] = None,
                 label_types: Optional[List[Type[Label]]] = None):
        # TODO[B4]: handle feature types (if not provided, gather all from events. Also: pre-compute feature values
        self.logger = logging.getLogger(__name__)
        self.events: List[E] = events
        self.feature_types: List[Type[Feature]] = (feature_types if feature_types is not None
                                                   else self.compute_feature_types(events))
        self.label_types: List[Type[Label]] = (label_types if label_types is not None
                                               else self.compute_label_types(events))

    def __len__(self):
        return len(self.events)

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> 'Corpus':
        """ """

    @classmethod
    @abstractmethod
    def load(cls, filepath: str, volatile: bool = False, **kwargs) -> 'Corpus':
        """ :raises IOError if file at `filepath` doesn't exist or is an invalid file type
                    CorpusError if fails to load corpus (for example if it uses an outdated format)
                    ResourceError if fails to locate additional resources (audio files, annotations, etc.) """

    @abstractmethod
    def export(self, filepath: str, overwrite: bool = False, **kwargs) -> None:
        """ :raises IOError if unable to write to file or if file already exists and `overwrite` is False. """

    @abstractmethod
    def append(self, event: E) -> None:
        """ """

    @staticmethod
    def compute_feature_types(events: List[E]) -> List[Type[Feature]]:
        raise NotImplemented("Not implemented")  # TODO[B6]

    @staticmethod
    def compute_label_types(events: List[E]) -> List[Type[Label]]:
        raise NotImplemented("Not implemented")  # TODO[B6]

    def get_features_of_type(self, feature_type: Type[Feature]) -> List[Feature]:
        return [e.get_feature(feature_type) for e in self.events]


class FreeCorpus(Corpus[CorpusEvent]):

    @classmethod
    def build(cls, *args, **kwargs) -> 'Corpus':
        raise NotImplemented("Not implemented")  # TODO[B6]

    @classmethod
    def load(cls, filepath: str, volatile: bool = False, **kwargs) -> 'Corpus':
        raise NotImplemented("Not implemented")  # TODO[B6]

    def export(self, filepath: str, overwrite: bool = False, **kwargs) -> None:
        raise NotImplemented("Not implemented")  # TODO[B6]

    def append(self, event: E) -> None:
        for feature in event.features:
            if feature not in self.feature_types:
                raise CorpusError(f"Feature {feature.__class__.__name__} does not exist in corpus {self}. "
                                  f"Could not add event")
        for label in event.labels:
            if label not in self.label_types:
                raise CorpusError(f"Label {label.__class__.__name__} does not exist in corpus {self}. "
                                  f"Could not add event")
