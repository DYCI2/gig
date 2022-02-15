import logging
from abc import ABC, abstractmethod
from typing import List

from main.corpus import Corpus
from main.corpus_event import CorpusEvent
from main.generator import Generator
from main.query import Query
from stubs.rendering import Message
from stubs.time import Time


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

    def read_memory(self, corpus: Corpus, **kwargs) -> None:
        self.clear()
        self.generator.read_memory(corpus, **kwargs)

    def learn_event(self, event: CorpusEvent, **kwargs) -> None:
        self.generator.learn_event(event, **kwargs)

    def clear(self) -> None:
        raise NotImplementedError("This needs to handle scheduling & state flushing")


class Dyci2GenerationScheduler(GenerationScheduler):
    """ """

    def __init__(self):
        super().__init__()

    def process_query(self, query: Query, **kwargs) -> None:
        pass

    def update_time(self, time: Time) -> List[Message]:
        pass


class SomaxGenerationScheduler(GenerationScheduler):
    """ """

    def __init__(self):
        super().__init__()

    def process_query(self, query: Query, **kwargs) -> None:
        pass

    def update_time(self, time: Time) -> List[Message]:
        pass
