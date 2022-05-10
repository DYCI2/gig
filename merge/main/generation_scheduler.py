from abc import ABC, abstractmethod

from merge.main.corpus import Corpus
from merge.main.corpus_event import CorpusEvent
from merge.main.query import Query


class GenerationScheduler(ABC):
    """ """

    @abstractmethod
    def process_query(self, query: Query, **kwargs) -> None:
        """ """

    # @abstractmethod
    # def update_time(self, time: Time) -> List[Message]:
    #     """ """

    @abstractmethod
    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        """ """

    @abstractmethod
    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """
