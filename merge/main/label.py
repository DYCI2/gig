from abc import ABC


class Label(ABC):
    pass  # TODO: Empty interface for now


class IntLabel:
    def __init__(self, label: int):
        self.label: int = label


class ListLabel:
    pass  # TODO: DYCI2 implementation


class ChordLabel:
    pass  # TODO: DYCI2 implementation
