import asyncio
import ipaddress
import logging
import multiprocessing
from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional, Callable, List, Awaitable

from maxosc.caller import Caller
from maxosc.maxformatter import MaxFormatter
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

from merge.io.osc_sender import OscSender
from merge.stubs.rendering import Renderable


class AsyncOsc(Caller, ABC):
    IP_LOCALHOST = "127.0.0.1"
    DEFAULT_CALLBACK_INTERVAL = 0.001

    def __init__(self,
                 recv_port: int,
                 send_port: int,
                 ip: str,
                 default_address: str,
                 discard_duplicate_args: bool = False,
                 reraise_exceptions: bool = True,
                 *args, **kwargs):
        super().__init__(discard_duplicate_args=discard_duplicate_args, *args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.recv_port: int = recv_port
        self.send_port: int = send_port
        self.ip: str = ip
        self.default_address: str = default_address
        self.reraise_exceptions: bool = reraise_exceptions

        self._sender: OscSender = OscSender(ip, send_port)

        self.server: Optional[AsyncIOOSCUDPServer] = None

        self._async_targets: List[Callable[[], Awaitable[None]]] = []
        self.__running: bool = False

    @abstractmethod
    async def _main_loop(self):
        """ Main loop function """

    async def _run_until_terminated(self) -> None:
        """ Dummy main loop to use for applications that do not need any async processing apart from OSC
            To use:
            >>> class MyServer(AsyncOsc):
            >>>     async def _main_loop(self):
            >>>         await self._run_until_terminated()
            """
        while self.running:
            await asyncio.sleep(1.0)

    def start(self) -> None:
        """ Main function used to start the object. Function named for consistency with multiprocessing.Process """
        if isinstance(self, multiprocessing.Process):
            multiprocessing.Process.start(self)
        else:
            self.run()

    def run(self) -> None:
        """ Override this function if more complex error handling is needed.
            Again, function is named for compatibility with multiprocessing.Process
            Note: NEVER CALL THIS FUNCTION EXPLICITLY, ALWAYS CALL `start` """
        try:
            asyncio.run(self._run())
        except OSError as e:
            self.logger.critical(f"{str(e)}. Could not run object")
            self.stop()
        except KeyboardInterrupt:
            self.logger.critical(f"Terminating due to keyboard interrupt (SIGINT)")
            self.stop()

    def stop(self) -> None:
        self.__running = False

    def add_async_target(self, func: Callable[[], Awaitable[None]]) -> None:
        """ Add additional async functions to call continuously running. Each function needs their own loop
        and should utilize `self.running` ideally. See `AsyncWithStatus` below """
        if not self.running:
            self._async_targets.append(func)
        else:
            raise RuntimeError("Cannot add async target while already running")

    def send(self, *args, address: Optional[str] = None) -> None:
        address = address if address is not None else self.default_address
        if len(args) == 1 and isinstance(args[0], Renderable):
            self._sender.send_renderable(address, args[0])
        else:
            self._sender.send(address, *args)

    @property
    def running(self):
        """ Note: Should be used to control main loop """
        return self.__running

    async def _run(self) -> None:
        """ raises: OSError is server already is in use """
        self.__running = True
        osc_dispatcher: Dispatcher = Dispatcher()
        osc_dispatcher.map(self.default_address, self.__process_osc)
        osc_dispatcher.set_default_handler(self.__unmatched_osc)
        self.server: AsyncIOOSCUDPServer = AsyncIOOSCUDPServer((self.ip, self.recv_port),
                                                               osc_dispatcher, asyncio.get_event_loop())
        transport, protocol = await self.server.create_serve_endpoint()
        await asyncio.gather(self._main_loop(), *[f() for f in self._async_targets])
        transport.close()

    def __process_osc(self, _address, *args):
        args_str: str = MaxFormatter.format_as_string(*args)
        try:
            self.call(args_str)
        except Exception as e:
            self.logger.error(e)
            self.logger.debug(repr(e))
            if self.reraise_exceptions:
                raise

    def __unmatched_osc(self, address: str, *_args, **_kwargs) -> None:
        self.logger.info(f"The address '{address}' does not exist.")

    @staticmethod
    def parse_ip(ip: str, logger: Optional[Logger] = None) -> str:
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError as e:
            err = f"{str(e)}. Setting ip to {AsyncOsc.IP_LOCALHOST}."
            logger.error(err)
            return AsyncOsc.IP_LOCALHOST

    @staticmethod
    def path_to_osc_address(component_path: List[str]) -> str:
        return "/" + "/".join(component_path)

    @staticmethod
    def osc_address_to_path(osc_address: str) -> List[str]:
        if osc_address.startswith("/"):
            return osc_address.split("/")[1:]
        return osc_address.split()


class AsyncOscMPC(AsyncOsc, multiprocessing.Process, ABC):
    def __init__(self, *args, **kwargs):
        # It's critical that multiprocessing.Process is initialized without any arguments
        # and that `AsyncOscWithStatus` is declared first in the __mro__
        AsyncOsc.__init__(self, *args, **kwargs)
        multiprocessing.Process.__init__(self)
