import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from merge.corpus import Corpus
from merge.main.candidate import Candidate
from merge.main.corpus_event import CorpusEvent
from merge.main.jury import Jury
from merge.main.merge_handler import MergeHandler
from merge.main.post_filter import PostFilter
from merge.main.prospector import Prospector
from merge.main.query import Query


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

    def _on_feedback(self, event: Optional[Candidate], **kwargs) -> None:
        """ Override this function to implement manual behaviour on feedback """
        pass

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
