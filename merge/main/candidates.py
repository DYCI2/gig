from abc import ABC, abstractmethod
from typing import List, Type, Union, Optional

import numpy as np

from merge.main.candidate import Candidate
from merge.main.feature import Feature
from merge.stubs.transform import Transform


class Candidates(ABC):

    # TODO[B2] This cannot be implemented until we have a good solution for transforms
    # @classmethod
    # @abstractmethod
    # def create_empty(cls, associated_corpus: Corpus, *args, **kwargs) -> 'Candidates':
    #     """ """

    @classmethod
    @abstractmethod
    def copy(cls, other) -> 'Candidates':
        """ :raises TypeError if trying to copy `Candidates` as an invalid type. """

    @abstractmethod
    def add(self, candidates: List[Candidate], **kwargs) -> None:
        """ :raises CorpusError if adding candidates that violate Corpus constraints of Candidates subclasses """

    @abstractmethod
    def get_feature_array(self, feature: Union[Type[Feature], str]) -> np.ndarray:
        """ """

    @abstractmethod
    def get_candidate(self, index: int) -> Candidate:
        """ """

    @abstractmethod
    def get_candidates(self) -> List[Candidate]:
        """ """

    @abstractmethod
    def get_scores(self) -> np.ndarray:
        """ """

    @abstractmethod
    def get_indices(self) -> np.ndarray:
        """ """

    @abstractmethod
    def get_transforms(self) -> List[Transform]:
        """ """

    @abstractmethod
    def normalize(self, norm: float = 1.0) -> None:
        """ """

    @abstractmethod
    def remove(self, indices: Union[int, np.ndarray]) -> None:
        """ :raises IndexError if an index is out of bounds """

    @abstractmethod
    def is_empty(self) -> bool:
        """ """

    @abstractmethod
    def size(self) -> int:
        """ """

    @abstractmethod
    def scale(self, factors: Union[float, np.ndarray], indices: Optional[np.ndarray] = None) -> None:
        """ TODO: Proper docstring
            factors: should either be
                a scalar (float) or
                an array of the same shape as the content returned from `get_candidates`, `get_scores`, etc. or
                an array of factors (any shape) in combination with an index map (of same shape)
            indices: can be either
                an array of indices in combination with an array of factors (same shape)
                a boolean mask of the same shape as the content returned from `get_candidates`, `get_scores`, etc.

            The operation performed if `indices` are provided is equivalent to
            ```
                self.score[indices] *= factors
            ```
        """


class BaseCandidates(Candidates):
    pass


class DiscreteCandidates(Candidates):
    pass # TODO: Implementation ongoing in somax.peaks



class MatrixCandidates(Candidates):
    pass
