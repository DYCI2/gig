class RelativeSchedulable:
    pass


class AbsoluteSchedulable:
    pass


class CorpusEvent:
    pass


class MidiEvent(CorpusEvent, RelativeSchedulable, AbsoluteSchedulable):
    pass


class AudioEvent(CorpusEvent, AbsoluteSchedulable):
    pass


class BeatAudioEvent(AudioEvent, RelativeSchedulable):
    pass
