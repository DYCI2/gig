import logging
from typing import Dict, Union, Type, List, Optional

from merge.main.feature import Feature
from merge.main.label import Label
from merge.stubs.note import Note


class RelativeSchedulable:
    def __init__(self, relative_onset: float, relative_duration: float, tempo: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relative_onset: float = relative_onset
        self.relative_duration: float = relative_duration
        self.tempo: float = tempo


class AbsoluteSchedulable:
    def __init__(self, absolute_onset: float, absolute_duration: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.absolute_onset: float = absolute_onset
        self.absolute_duration: float = absolute_duration


class CorpusEvent:
    def __init__(self, index: int,
                 features: Dict[Union[str, Type[Feature]], Feature],
                 labels: Dict[Union[str, Type[Label]], Label],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.index: int = index
        self.features: Dict[Union[str, Type[Feature]], Feature] = features
        self.labels: Dict[Union[str, Type[Label]], Label] = labels

    def get_feature(self, feature_type: Union[str, Type[Feature]]) -> Optional[Feature]:
        return self.features.get(feature_type)

    def get_label(self, label_type: Union[str, Type[Label]]) -> Optional[Label]:
        return self.labels.get(label_type)


class MidiEvent(CorpusEvent, RelativeSchedulable, AbsoluteSchedulable):
    def __init__(self, index: int,
                 features: Dict[Union[str, Type[Feature]], Feature],
                 labels: Dict[Union[str, Type[Label]], Label],
                 relative_onset: float, relative_duration: float, tempo: float,
                 absolute_onset: float, absolute_duration: float,
                 notes: List[Note]):
        super().__init__(index=index, features=features, labels=labels,
                         relative_onset=relative_onset, relative_duration=relative_duration, tempo=tempo,
                         absolute_onset=absolute_onset, absolute_duration=absolute_duration)
        self.notes: List[Note] = notes


class AudioEvent(CorpusEvent, AbsoluteSchedulable):
    def __init__(self, index: int,
                 features: Dict[Union[str, Type[Feature]], Feature],
                 labels: Dict[Union[str, Type[Label]], Label],
                 absolute_onset: float, absolute_duration: float):
        super().__init__(index=index, features=features, labels=labels,
                         absolute_onset=absolute_onset, absolute_duration=absolute_duration)


class BeatAudioEvent(AudioEvent, RelativeSchedulable):
    def __init__(self, index: int,
                 features: Dict[Union[str, Type[Feature]], Feature],
                 labels: Dict[Union[str, Type[Label]], Label],
                 relative_onset: float, relative_duration: float, tempo: float,
                 absolute_onset: float, absolute_duration: float):
        super().__init__(index=index, features=features, labels=labels,
                         relative_onset=relative_onset, relative_duration=relative_duration, tempo=tempo,
                         absolute_onset=absolute_onset, absolute_duration=absolute_duration)