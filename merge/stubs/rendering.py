from abc import abstractmethod
from typing import Union, List, Any, Iterable


class RendererMessage:
    def __init__(self, *args):
        self.message: Iterable[Any] = args


class Renderable:


    @abstractmethod
    def render(self) -> Union[List[RendererMessage], RendererMessage]:
        """ Format the object into one or multiple renderable messages that may be sent over OSC """
