from abc import ABC
from collections.abc import Iterable
from typing import TypeVar, Generic, List, Union, Type, Any

from merge.main.corpus_event import CorpusEvent
from merge.main.descriptor import Descriptor
from merge.main.label import Label

T = TypeVar('T')


class Influence(Generic[T], ABC):
    def __init__(self, value: T):
        self.value = value

    @classmethod
    def from_triggers(cls, n_triggers: int) -> List['Influence']:
        return [NoInfluence() for _ in range(n_triggers)]

    @classmethod
    def from_events(cls, events: Union[CorpusEvent, List[CorpusEvent]]) -> List['Influence']:
        return cls._from_type_or_iterable(value_type=CorpusEvent, influence_type=CorpusInfluence, data=events)

    @classmethod
    def from_descriptors(cls, descriptors: Union[Descriptor, List[Descriptor]]) -> List['Influence']:
        return cls._from_type_or_iterable(value_type=Descriptor, influence_type=DescriptorInfluence, data=descriptors)

    @classmethod
    def from_labels(cls, labels: Union[Label, List[Label]]) -> List['Influence']:
        return cls._from_type_or_iterable(value_type=Label, influence_type=LabelInfluence, data=labels)

    @classmethod
    def _from_type_or_iterable(cls,
                               value_type: Type[T],
                               influence_type: Type['Influence'],
                               data: Union[T, List[T]]) -> List['Influence']:
        if isinstance(data, value_type):
            return [influence_type(value=data)]
        else:
            return [influence_type(value=e) for e in data]


class NoInfluence(Influence[None]):
    """ Class to trigger incrementation of state without any external requirements to match """

    def __init__(self, value: None = None):
        super().__init__(value=value)


class CorpusInfluence(Influence[CorpusEvent]):
    """ Class to trigger incrementation of state based on a `CorpusEvent` """
    pass


class DescriptorInfluence(Influence[Descriptor]):
    """ Class to trigger incrementation of state based on a `Feature` """
    pass


class LabelInfluence(Influence[Label]):
    """ Class to trigger incrementation of state based on a `Label` """
    pass

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"
