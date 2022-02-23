from abc import ABC, abstractmethod
from typing import Optional

from merge.main.candidate import Candidate
from merge.main.candidates import Candidates


class PostFilter(ABC):

    @abstractmethod
    def filter(self, candidates: Candidates) -> Candidates:
        """ """

    @abstractmethod
    def feedback(self, candidate: Optional[Candidate], **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """
