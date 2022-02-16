from typing import Optional

from merge.main.corpus_event import CorpusEvent
from merge.stubs.transform import Transform


class Candidate:
    def __init__(self, event: CorpusEvent, score: float, transform: Optional[Transform] = None):
        self.event: CorpusEvent = event
        self.score: float = score
        self.transform: Optional[Transform] = transform

