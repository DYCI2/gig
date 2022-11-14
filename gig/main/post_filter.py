from abc import ABC, abstractmethod
from typing import Optional

from gig.io.parsable import Parsable
from gig.main.candidate import Candidate
from gig.main.candidates import Candidates


class PostFilter(Parsable, ABC):

    @abstractmethod
    def filter(self, candidates: Candidates) -> Candidates:
        """ """

    @abstractmethod
    def feedback(self, candidate: Optional[Candidate], **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """
