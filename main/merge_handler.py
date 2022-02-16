from abc import ABC, abstractmethod
from typing import List, Optional

from main.candidates import Candidates


class MergeHandler(ABC):

    @abstractmethod
    def merge(self, candidates: List[Candidates]) -> Candidates:
        """ """

    @abstractmethod
    def feedback(self, event: Optional[Candidates], **kwargs) -> None:
        """ """

    @abstractmethod
    def clear(self) -> None:
        """ """
