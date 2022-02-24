from abc import ABC
from typing import TypeVar, Generic, List, Union

from merge.main.corpus_event import CorpusEvent
from merge.main.exceptions import QueryError
from merge.main.feature import Feature
from merge.main.label import Label

# T = TypeVar('T')
#
#
# class Influence(Generic[T], ABC):
#     def __init__(self, data: Union[T, List[T]]):
#         if not isinstance(data, list):
#             self.data: List[T] = [data]
#         elif len(data) == 0:
#             raise QueryError(f"A {self.__class__.__name__} cannot be empty.")
#         else:
#             self.data: List[T] = data
#
#     def __len__(self) -> int:
#         return len(self.data)
#
#
# class CorpusInfluence(Influence[CorpusEvent]):
#     pass
#
#
# class FeatureInfluence(Influence[Feature]):
#     pass
#
#
# class LabelInfluence(Influence[Label]):
#     pass
#
#
# class TriggerInfluence(Influence[None]):
#     pass
