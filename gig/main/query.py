import logging
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, List, Union

from gig.main.exceptions import QueryError
from gig.main.influence import Influence
from gig.stubs.pathspec import PathSpec
from gig.stubs.timepoint import Timepoint

T = TypeVar('T')


class Query(Generic[T], ABC):
    def __init__(self, content: T, time: Optional[Timepoint] = None, path: Optional[PathSpec] = None):
        self.logger = logging.getLogger(__name__)
        self.content: T = content
        self.time: Optional[Timepoint] = time
        self.path: Optional[PathSpec] = path

    @abstractmethod
    def __len__(self) -> int:
        """ """

    def __repr__(self):
        return f"{self.__class__.__name__}(labels={self.content},time={self.time},path={self.path})"


class TriggerQuery(Query[int], ABC):
    """ Integer `data` specifies number of events to trigger """

    def __init__(self, content: int = 1, time: Optional[Timepoint] = None, path: Optional[PathSpec] = None):
        super().__init__(content, time, path)
        if content <= 0:
            raise QueryError(f"A {self.__class__.__name__} must trigger at least 1 event. Actual: {content}")

    def __len__(self) -> int:
        return self.content


class InfluenceQuery(Query[List[Influence]]):
    def __init__(self,
                 content: Union[Influence, List[Influence]],
                 time: Optional[Timepoint] = None,
                 path: Optional[PathSpec] = None):
        super().__init__(content, time, path)

        if not isinstance(content, list):
            self.content: List[Influence] = [content]
        elif len(content) == 0:
            raise QueryError(f"A {self.__class__.__name__} cannot be empty.")
        else:
            self.content: List[Influence] = content

    def __len__(self) -> int:
        return len(self.content)

# class FeatureQuery(InfluenceQuery[Feature]):
#     pass
#
#
# class LabelQuery(InfluenceQuery[Label]):
#     pass
#
#
# class CorpusQuery(InfluenceQuery[CorpusEvent]):
#     pass
