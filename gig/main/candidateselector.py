from abc import ABC, abstractmethod
from typing import Optional

from gig.main.candidate import Candidate
from gig.main.candidates import Candidates


class CandidateSelector(ABC):

    @abstractmethod
    def decide(self, candidates: Candidates) -> Optional[Candidate]:
        """ """

    @abstractmethod
    def feedback(self, candidate: Optional[Candidate], **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """
