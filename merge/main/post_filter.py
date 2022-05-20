from abc import ABC, abstractmethod
from typing import Optional

from merge.io.parsable import Parsable
from merge.main.candidate import Candidate
from merge.main.candidates import Candidates


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
