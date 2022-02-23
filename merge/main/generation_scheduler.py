import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from merge.corpus import Corpus
from merge.main.candidate import Candidate
from merge.main.corpus_event import CorpusEvent
from merge.main.generator import Generator
from merge.main.query import Query
from merge.stubs.rendering import Message
from merge.stubs.time import Time


class GenerationScheduler(ABC):
    """ """

    def __init__(self, generator: Generator):
        self.logger = logging.getLogger(__name__)
        self.generator: Generator = generator

    @abstractmethod
    def process_query(self, query: Query, **kwargs) -> None:
        """ """

    @abstractmethod
    def update_time(self, time: Time) -> List[Message]:
        """ """

    def _on_feedback(self, event: Optional[Candidate], **kwargs) -> None:
        """ Override this function to implement manual behaviour on feedback """
        pass

    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        self.clear()
        self.generator.read_memory(corpus, **kwargs)

    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        self.generator.learn_event(event, **kwargs)

    def clear(self) -> None:
        raise NotImplementedError("This needs to handle scheduling & state flushing")

    def feedback(self, event: Optional[Candidate], **kwargs) -> None:
        self._on_feedback(event, **kwargs)
        self.generator.feedback(event, **kwargs)


class Dyci2GenerationScheduler(GenerationScheduler):
    """ """

    def __init__(self):
        super().__init__()

    def update_state(self, query: Query, **kwargs) -> None:
        pass

    def update_time(self, time: Time) -> List[Message]:
        pass


class SomaxGenerationScheduler(GenerationScheduler):
    """ """

    def __init__(self):
        super().__init__()

    def update_state(self, query: Query, **kwargs) -> None:
        pass

    def update_time(self, time: Time) -> List[Message]:
        pass
