import logging
from typing import Dict, Union, Type, List, Optional, Generic, TypeVar

from merge.main.exceptions import FeatureError, LabelError
from merge.main.feature import Feature
from merge.main.label import Label
from merge.stubs.note import Note

T = TypeVar('T')


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
    def __init__(self,
                 index: int,
                 features: Optional[Dict[Union[str, Type[Feature]], Feature]] = None,
                 labels: Optional[Dict[Union[str, Type[Label]], Label]] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.index: int = index
        self.features: Dict[Union[str, Type[Feature]], Feature] = features if features is not None else {}
        self.labels: Dict[Union[str, Type[Label]], Label] = labels if labels is not None else {}

    def __repr__(self):
        if (len(self.features) == 1 and len(self.labels) == 0) or (len(self.features) == 0 and len(self.labels) == 1):
            return f"{self.__class__.__name__}(index={self.index},features={self.features},labels={self.labels})"
        else:
            return f"{self.__class__.__name__}(index={self.index},features=...,labels=...)"

    def get_feature(self, feature_type: Union[str, Type[Feature]]) -> Feature:
        try:
            return self.features[feature_type]
        except KeyError as e:
            raise FeatureError(f"Event '{str(self)}' does not have a feature of type '{feature_type.__name__}'") from e

    def get_label(self, label_type: Union[str, Type[Label]]) -> Optional[Label]:
        try:
            return self.labels[label_type]
        except KeyError as e:
            raise FeatureError(f"Event '{str(self)}' does not have a label of type '{label_type.__name__}'") from e


class GenericCorpusEvent(CorpusEvent, Generic[T]):
    def __init__(self,
                 data: T,
                 index: int,
                 features: Optional[Dict[Union[str, Type[Feature]], Feature]] = None,
                 labels: Optional[Dict[Union[str, Type[Label]], Label]] = None,
                 **kwargs):
        super().__init__(index=index, features=features, labels=labels, **kwargs)
        self.data: T = data


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
