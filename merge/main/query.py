import logging
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, List

from merge.main.corpus_event import CorpusEvent
from merge.main.exceptions import QueryError
from merge.main.feature import Feature
from merge.main.label import Label
from merge.stubs.pathspec import PathSpec
from merge.stubs.time import Time

T = TypeVar('T')


class Query(Generic[T], ABC):
    def __init__(self, content: T, time: Optional[Time] = None, path: Optional[PathSpec] = None):
        self.logger = logging.getLogger(__name__)
        self.content: T = content
        self.time: Optional[Time] = time
        self.path: Optional[PathSpec] = path

    @abstractmethod
    def __len__(self) -> int:
        """ """

    def __repr__(self):
        return f"{self.__class__.__name__}(labels={self.content},time={self.time},path={self.path})"


class TriggerQuery(Query[int], ABC):
    """ Integer `data` specifies number of events to trigger """

    def __init__(self, content: int = 1, time: Optional[Time] = None, path: Optional[PathSpec] = None):
        super().__init__(content, time, path)
        if content <= 0:
            raise QueryError(f"A {self.__class__.__name__} must trigger at least 1 event. Actual: {content}")

    def __len__(self) -> int:
        return self.content


class InfluenceQuery(Generic[T], Query[List[T]]):
    def __init__(self, content: List[T], time: Optional[Time] = None, path: Optional[PathSpec] = None):
        super().__init__(content, time, path)
        if len(content) == 0:
            raise QueryError(f"A {self.__class__.__name__} must contain at least one element")

    def __len__(self) -> int:
        return len(self.content)


class FeatureQuery(InfluenceQuery[Feature]):
    pass


class LabelQuery(InfluenceQuery[Label]):
    pass


class CorpusQuery(InfluenceQuery[CorpusEvent]):
    pass
