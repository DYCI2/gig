from typing import Optional

from main.corpus_event import CorpusEvent
from stubs.transform import Transform


class Candidate:
    def __init__(self, event: CorpusEvent, score: float, transform: Optional[Transform] = None):
        self.event: CorpusEvent = event
        self.score: float = score
        self.transform: Optional[Transform] = transform

