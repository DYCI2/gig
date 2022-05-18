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


class OscLogForwarder(logging.Handler):

    def __init__(self, sender: OscSender, osc_log_address: str, logging_level: int = logging.INFO):
        super().__init__()
        self.sender: OscSender = sender
        self.osc_log_address: str = osc_log_address
        self.setLevel(logging_level)

    def emit(self, record):
        self.sender.send(self.osc_log_address, record.levelname.lower(), self.format(record))

    def set_log_level(self, logging_level: int):
        self.setLevel(logging_level)
