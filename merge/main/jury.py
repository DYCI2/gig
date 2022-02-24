from abc import ABC, abstractmethod
from typing import Optional

from merge.main.candidate import Candidate
from merge.main.candidates import Candidates


class Jury(ABC):

    @abstractmethod
    def decide(self, candidates: Candidates) -> Optional[Candidate]:
        """ """

    @abstractmethod
    def feedback(self, candidate: Optional[Candidate], **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """
