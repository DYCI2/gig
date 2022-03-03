from typing import Optional, Union

from merge.corpus import Corpus
from merge.main.corpus_event import CorpusEvent
from merge.stubs.transform import Transform


class Candidate:
    # TODO[B2]: Transform should not allow passing a single integer, only the Transform object.
    #           Temporary like this until B2
    def __init__(self, event: CorpusEvent, score: float, transform: Optional[Union[Transform, int]],
                 associated_corpus: Corpus):
        self.event: CorpusEvent = event
        self.score: float = score
        self.transform: Optional[Union[Transform, int]] = transform  # TODO[B2]: NoTransform if Optional
        self.associated_corpus: Corpus = associated_corpus

    def __repr__(self):
        return f"{self.__class__.__name__}(event={self.event},score={self.score},transform={self.transform},...)"

    @classmethod
    def new_default(cls, event: CorpusEvent, associated_corpus: Corpus) -> 'Candidate':
        return cls(event=event, score=1.0, transform=None, associated_corpus=associated_corpus)

    def shallow_copy(self) -> 'Candidate':
        """ Create a shallow copy (to avoid rewriting the score the internal state """
        return Candidate(self.event, self.score, self.transform, self.associated_corpus)
