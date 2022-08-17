import logging
from typing import Dict, Union, Type, List, Optional, Generic, TypeVar

from merge.main.descriptor import Descriptor
from merge.main.exceptions import DescriptorError, LabelError
from merge.main.label import Label
from merge.stubs.note import Note

T = TypeVar('T')


class RelativeSchedulable:
    """ Interface for events that may be scheduled in relative time (ticks) """

    def __init__(self, relative_onset: float, relative_duration: float, tempo: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relative_onset: float = relative_onset
        self.relative_duration: float = relative_duration
        self.tempo: float = tempo


class AbsoluteSchedulable:
    """ Interface for events that may be scheduled in absolute time (seconds) """

    def __init__(self, absolute_onset: float, absolute_duration: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.absolute_onset: float = absolute_onset
        self.absolute_duration: float = absolute_duration


class CorpusEvent:
    def __init__(self,
                 index: int,
                 descriptors: Optional[Dict[Union[str, Type[Descriptor]], Descriptor]] = None,
                 labels: Optional[Dict[Union[str, Type[Label]], Label]] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.index: int = index
        self.descriptors: Dict[Union[str, Type[Descriptor]], Descriptor]
        self.descriptors = descriptors if descriptors is not None else {}
        self.labels: Dict[Union[str, Type[Label]], Label] = labels if labels is not None else {}

    def __repr__(self):
        if (len(self.descriptors) == 1 and len(self.labels) == 0) \
                or (len(self.descriptors) == 0 and len(self.labels) == 1):
            return f"{self.__class__.__name__}(index={self.index},descriptors={self.descriptors},labels={self.labels})"
        else:
            return f"{self.__class__.__name__}(index={self.index},descriptors=...,labels=...)"

    def get_descriptor(self, descriptor_type: Union[str, Type[Descriptor]]) -> Descriptor:
        try:
            return self.descriptors[descriptor_type]
        except KeyError as e:
            raise DescriptorError(f"Event '{str(self)}' does not have a descriptor of "
                                  f"type '{descriptor_type.__name__}'") from e

    def get_label(self, label_type: Union[str, Type[Label]]) -> Optional[Label]:
        try:
            return self.labels[label_type]
        except KeyError as e:
            raise LabelError(f"Event '{str(self)}' does not have a label of type '{label_type.__name__}'") from e


class GenericCorpusEvent(CorpusEvent, Generic[T]):
    def __init__(self,
                 data: T,
                 index: int,
                 descriptors: Optional[Dict[Union[str, Type[Descriptor]], Descriptor]] = None,
                 labels: Optional[Dict[Union[str, Type[Label]], Label]] = None,
                 **kwargs):
        super().__init__(index=index, descriptors=descriptors, labels=labels, **kwargs)
        self.data: T = data


class MidiEvent(CorpusEvent, RelativeSchedulable, AbsoluteSchedulable):
    def __init__(self,
                 index: int,
                 descriptors: Dict[Union[str, Type[Descriptor]], Descriptor],
                 labels: Dict[Union[str, Type[Label]], Label],
                 relative_onset: float,
                 relative_duration: float,
                 tempo: float,
                 absolute_onset: float,
                 absolute_duration: float,
                 notes: List[Note]):
        super().__init__(index=index,
                         descriptors=descriptors,
                         labels=labels,
                         relative_onset=relative_onset,
                         relative_duration=relative_duration,
                         tempo=tempo,
                         absolute_onset=absolute_onset,
                         absolute_duration=absolute_duration)
        self.notes: List[Note] = notes


class AudioEvent(CorpusEvent, AbsoluteSchedulable):
    def __init__(self,
                 index: int,
                 descriptors: Dict[Union[str, Type[Descriptor]], Descriptor],
                 labels: Dict[Union[str, Type[Label]], Label],
                 absolute_onset: float,
                 absolute_duration: float):
        super().__init__(index=index,
                         descriptors=descriptors,
                         labels=labels,
                         absolute_onset=absolute_onset,
                         absolute_duration=absolute_duration)


class BeatAudioEvent(AudioEvent, RelativeSchedulable):
    def __init__(self,
                 index: int,
                 descriptors: Dict[Union[str, Type[Descriptor]], Descriptor],
                 labels: Dict[Union[str, Type[Label]], Label],
                 relative_onset: float,
                 relative_duration: float,
                 tempo: float,
                 absolute_onset: float,
                 absolute_duration: float):
        super().__init__(index=index,
                         descriptors=descriptors,
                         labels=labels,
                         relative_onset=relative_onset,
                         relative_duration=relative_duration,
                         tempo=tempo,
                         absolute_onset=absolute_onset,
                         absolute_duration=absolute_duration)
