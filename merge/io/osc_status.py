import asyncio
import multiprocessing
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List

from maxosc import SendFormat, Sender

from merge.io.async_osc import AsyncOsc
from merge.io.component import Component


class Status(IntEnum):
    INVALID_STATUS = -1
    OFFLINE = 0
    PARENT_OBJ_MISSING = 1
    PARENT_OBJ_NOT_READY = 2
    UNINITIALIZED = 3
    INITIALIZING = 4
    READY = 5
    NO_RESPONSE = 6
    DELETED = 7
    WORKING = 8
    TERMINATED = 9


class AsyncOscWithStatus(AsyncOsc, ABC):
    STATUS_OSC_ADDRESS = "status"

    def __init__(self,
                 recv_port: int,
                 send_port: int,
                 ip: str,
                 default_address: str,
                 discard_duplicate_args: bool = False,
                 osc_send_format: SendFormat = SendFormat.FLATTEN,
                 reraise_exceptions: bool = True,
                 status_send_interval_s: float = 0.5,
                 *args, **kwargs):
        super().__init__(recv_port, send_port, ip, default_address, discard_duplicate_args,
                         osc_send_format, reraise_exceptions, *args, **kwargs)
        self.status_sender: Sender = Sender(ip, send_port)
        self.status_send_interval: float = status_send_interval_s

        self.add_async_target(self._run_status_loop)

    @abstractmethod
    def get_main_component(self) -> Component:
        """ """

    def send_status_to_all(self, status: Status) -> None:
        for address, _ in self.get_main_component().get_components():
            self.send_status_to(address, status)

    def send_status_to(self, component_address: List[str], status: Status):
        status_address: str = self.path_to_osc_address(component_address + [AsyncOscWithStatus.STATUS_OSC_ADDRESS])
        self.status_sender.send(status_address, status.value)

    async def _run_status_loop(self) -> None:
        while self.running:
            # Any existing component will by default be considered READY
            self.send_status_to_all(Status.READY)
            await asyncio.sleep(self.status_send_interval)

        self.send_status_to_all(Status.TERMINATED)


class AsyncOscMPCWithStatus(AsyncOscWithStatus, multiprocessing.Process, ABC):
    def __init__(self, *args, **kwargs):
        # It's critical that multiprocessing.Process is initialized without any arguments
        # and that `AsyncOscWithStatus` is declared first in the __mro__
        AsyncOscWithStatus.__init__(self, *args, **kwargs)
        multiprocessing.Process.__init__(self)
