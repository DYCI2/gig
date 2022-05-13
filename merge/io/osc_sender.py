import collections.abc
import logging
from typing import Union, List

from maxosc.maxformatter import MaxFormatter
from pythonosc.udp_client import SimpleUDPClient

from merge.stubs.rendering import Renderable, RendererMessage


class OscSender:
    def __init__(self, ip: str, port: int):
        self.logger = logging.getLogger(__name__)
        self.ip: str = ip
        self.port: int = port
        self._client: SimpleUDPClient = SimpleUDPClient(address=ip, port=port)

    def send(self, address: str, *args) -> None:
        self._client.send_message(address, MaxFormatter.flatten(args, cnmat_compatibility=False))

    def send_renderable(self, address: str, renderable: Renderable) -> None:
        messages: Union[RendererMessage, List[RendererMessage]] = renderable.render()
        if isinstance(messages, RendererMessage):
            self._client.send_message(address, *messages.message)
        elif isinstance(messages, collections.abc.Iterable):
            for message in messages:  # type: RendererMessage
                self._client.send_message(address, *message.message)
