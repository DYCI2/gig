import logging
from abc import ABC, abstractmethod
from typing import Optional, List

from merge.corpus import Corpus
from merge.main.candidate import Candidate
from merge.main.candidates import Candidates
from merge.main.corpus_event import CorpusEvent
from merge.main.query import Query


class Prospector(ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        """ """

    @abstractmethod
    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        """ """

    @abstractmethod
    def process(self, query: Query, **kwargs) -> None:
        """ """

    @abstractmethod
    def peek_candidates(self) -> Candidates:
        """ # TODO: Proper docstring
            Get the candidates without modifying the prospector's internal state. Note that in most runtime cases,
            this behaviour is undesired. The candidates returned from `peek_candidates` should not be modified - they
            are not a copy. This should only be used to gather statistics, etc. """

    @abstractmethod
    def pop_candidates(self, **kwargs) -> Candidates:
        """ TODO: Proper docstring
            Note! Depending on implementation, may or may not remove or alter the candidates
                  in the prospector's internal state. """

    @abstractmethod
    def clear(self) -> None:
        """ """

    @abstractmethod
    def feedback(self, event: Optional[Candidate], **kwargs) -> None:
        """ """


class Dyci2Prospector(Prospector):
    pass
