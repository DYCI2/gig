from abc import ABC, abstractmethod
from typing import List, Any

from gig.main.corpus import Corpus
from gig.main.corpus_event import CorpusEvent
from gig.main.query import Query
from gig.stubs.timepoint import Timepoint


class GenerationScheduler(ABC):
    """ """

    @abstractmethod
    def process_query(self, query: Query, **kwargs) -> None:
        """ """

    @abstractmethod
    def update_performance_time(self, time: Timepoint) -> Any:
        """ TODO: Docstring
            raises: TimepointError if an invalid Timepoint is passed
        """

    @abstractmethod
    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        """ """

    @abstractmethod
    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """
