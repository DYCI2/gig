import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from main.candidate import Candidate
from main.corpus import Corpus
from main.corpus_event import CorpusEvent
from main.jury import Jury
from main.merge_handler import MergeHandler
from main.post_filter import PostFilter
from main.prospector import Prospector
from main.query import Query


class Generator(ABC):
    def __init__(self, prospectors: List[Prospector], merge_handler: MergeHandler, post_filters: List[PostFilter],
                 jury: Jury):
        self.logger = logging.getLogger(__name__)
        self._prospectors: List[Prospector] = prospectors
        self._merge_handler: MergeHandler = merge_handler
        self._post_filters: List[PostFilter] = post_filters  # TODO: Should be dict/component
        self._jury: Jury = jury

    @abstractmethod
    def process_query(self, query: Query, **kwargs) -> List[Optional[Candidate]]:
        pass

    @abstractmethod
    def _on_feedback(self, event: Optional[Candidate], **kwargs) -> None:
        """ """

    @abstractmethod
    def _on_clear(self) -> None:
        """ """

    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        # TODO: Handle multicorpus case: learning a corpus in only a particular Prospector => PathSpec argument
        for prospector in self._prospectors:
            prospector.read_memory(corpus, **kwargs)

    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        # TODO: Handle multicorpus case: learning a corpus in only a particular Prospector => PathSpec argument
        for prospector in self._prospectors:
            prospector.learn_event(event, **kwargs)

    def clear(self) -> None:
        self._on_clear()
        self._jury.clear()
        self._merge_handler.clear()

        for post_filter in self._post_filters:
            post_filter.clear()

        for prospector in self._prospectors:
            prospector.clear()

    def feedback(self, event: Optional[Candidate], **kwargs) -> None:
        self._on_feedback(event, **kwargs)
        self._jury.feedback(event, **kwargs)
        self._merge_handler.feedback(event, **kwargs)

        for post_filter in self._post_filters:
            post_filter.feedback(event, **kwargs)

        for prospector in self._prospectors:
            prospector.feedback(event, **kwargs)


class SomaxGenerator(Generator):
    pass


class Dyci2Generator(Generator):
    pass
