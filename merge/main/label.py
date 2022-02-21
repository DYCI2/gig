from abc import ABC


class Label(ABC):
    pass  # TODO: Empty interface for now


class IntLabel(Label):
    def __init__(self, label: int):
        self.label: int = label


class ListLabel(Label):
    pass  # TODO: DYCI2 implementation


class ChordLabel(Label):
    pass  # TODO: DYCI2 implementation
