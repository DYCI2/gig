from abc import ABC, abstractmethod
from typing import List, Optional

from merge.corpus import Corpus
from merge.main.candidate import Candidate
from merge.main.corpus_event import CorpusEvent
from merge.main.query import Query


class Generator(ABC):

    @abstractmethod
    def process_query(self, query: Query, **kwargs) -> List[Optional[Candidate]]:
        """ Query the Generator with new information in order to update its internal state """

    @abstractmethod
    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        """ """

    @abstractmethod
    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """

    @abstractmethod
    def feedback(self, event: Optional[Candidate], **kwargs) -> None:
        """ """
