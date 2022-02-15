from abc import ABC


class Corpus(ABC):
    pass


class FreeCorpus(Corpus):
    pass


class AudioCorpus(Corpus):
    pass


class MidiCorpus(Corpus):
    pass
