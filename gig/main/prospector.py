from abc import ABC, abstractmethod
from typing import Optional

from gig.main.corpus import Corpus
from gig.main.candidate import Candidate
from gig.main.candidates import Candidates
from gig.main.corpus_event import CorpusEvent
from gig.main.influence import Influence


class Prospector(ABC):

    @abstractmethod
    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        """ """

    @abstractmethod
    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        """ """

    @abstractmethod
    def process(self, influence: Influence, **kwargs) -> None:
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
            Get the candidates and (for most implementations) step forward in the Prospector's internal state. """

    @abstractmethod
    def clear(self) -> None:
        """ """

    @abstractmethod
    def feedback(self, event: Optional[Candidate], **kwargs) -> None:
        """ """
