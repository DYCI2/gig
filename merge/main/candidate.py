from typing import Optional, Union

from merge.corpus import Corpus
from merge.main.corpus_event import CorpusEvent
from merge.stubs.transform import Transform


class Candidate:
    # TODO[B2]: Transform should not allow passing a single integer, only the Transform object.
    #           Temporary like this until B2
    def __init__(self, event: CorpusEvent, score: float, transform: Optional[Union[Transform, int]] = None,
                 associated_corpus: Optional[Corpus] = None):
        self.event: CorpusEvent = event
        self.score: float = score
        self.transform: Optional[Union[Transform, int]] = transform
        self.associated_corpus: Optional[Corpus] = associated_corpus

