from abc import ABC, abstractmethod
from typing import List, Type, Union

import numpy as np

from merge.main.candidate import Candidate
from merge.main.feature import Feature
from merge.stubs.transform import Transform


class Candidates(ABC):

    @abstractmethod
    def get_feature(self, feature: Union[Type[Feature], str]) -> np.ndarray:
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
    def scale(self, factors: Union[float, np.ndarray]) -> None:
        """ TODO: Proper docstring
            factors: should either be a scalar (float) or the same shape as the content returned from
                     `get_candidates`, `get_scores`, etc. """


class DiscreteCandidates(Candidates):
    pass


class ContinuousCandidates(Candidates):
    def get_times(self) -> np.ndarray:
        pass


class MatrixCandidates(Candidates):
    pass
