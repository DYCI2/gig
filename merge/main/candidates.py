from abc import ABC, abstractmethod
from typing import List, Type, Union, Optional

import numpy as np

from merge.main.candidate import Candidate
from merge.main.exceptions import FeatureError
from merge.main.feature import Feature
from merge.stubs.transform import Transform


class Candidates(ABC):

    # TODO[B2] This cannot be implemented until we have a good solution for transforms
    # @classmethod
    # @abstractmethod
    # def create_empty(cls, associated_corpus: Corpus, *args, **kwargs) -> 'Candidates':
    #     """ """

    @abstractmethod
    def shallow_copy(self) -> 'Candidates':
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
    def __init__(self, candidates: List[Candidate]):
        self._candidates: List[Candidate] = candidates

    def shallow_copy(self) -> 'Candidates':
        return BaseCandidates([c.shallow_copy() for c in self._candidates])

    def add(self, candidates: List[Candidate], **kwargs) -> None:
        self._candidates.extend(candidates)

    def get_feature_array(self, feature: Union[Type[Feature], str]) -> np.ndarray:
        try:
            return np.array([c.event.get_feature(feature).value for c in self._candidates])
        except KeyError as e:
            raise FeatureError(e)

    def get_candidate(self, index: int) -> Candidate:
        return self._candidates[index]

    def get_candidates(self) -> List[Candidate]:
        return self._candidates

    def get_scores(self) -> np.ndarray:
        return np.array([c.score for c in self._candidates], dtype=np.int32)

    def get_indices(self) -> np.ndarray:
        return np.array([c.event.index for c in self._candidates], dtype=np.int32)

    def get_transforms(self) -> List[Transform]:
        return [c.transform for c in self._candidates]

    def normalize(self, norm: float = 1.0) -> None:
        scores: np.ndarray = np.array([c.score for c in self._candidates])
        if scores.size > 0:
            normalization_factor: float = norm / float(np.max(scores))
            for c in self._candidates:
                c.score *= normalization_factor

    def remove(self, indices: Union[int, np.ndarray]) -> None:
        if isinstance(indices, int):
            del self._candidates[indices]
        else:
            for index in sorted(indices, reverse=True):
                del self._candidates[index]

    def is_empty(self) -> bool:
        return len(self._candidates) == 0

    def size(self) -> int:
        return len(self._candidates)

    def scale(self, factors: Union[float, np.ndarray], indices: Optional[np.ndarray] = None) -> None:
        scores: np.ndarray = self.get_scores()
        if indices is not None:
            scores[indices] *= factors
        else:
            scores *= factors
        for c, s in zip(self._candidates, scores):  # type: Candidate, float
            c.score = s


class DiscreteCandidates(Candidates):
    pass  # TODO: Implementation ongoing in somax.peaks


class MatrixCandidates(Candidates):
    pass
