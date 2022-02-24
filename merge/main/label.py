from abc import ABC


class Label(ABC):
    pass  # TODO: Empty interface for now


class IntLabel(Label):
    def __init__(self, label: int):
        self.label: int = label

    def __repr__(self):
        return f"{self.__class__.__name__}(label={self.label})"


class ListLabel(Label):
    pass  # TODO: DYCI2 implementation


class ChordLabel(Label):
    pass  # TODO: DYCI2 implementation
