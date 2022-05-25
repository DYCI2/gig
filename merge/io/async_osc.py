import asyncio
import ipaddress
import logging
import multiprocessing
from abc import ABC, abstractmethod
from typing import Optional, Callable, List, Awaitable, Dict, Tuple

from maxosc.caller import Caller
from maxosc.exceptions import MaxOscError
from maxosc.maxformatter import MaxFormatter
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

from merge.io.component import Component
from merge.io.osc_sender import OscSender, OscLogForwarder
from merge.io.osc_status import Status
from merge.main.exceptions import ConfigurationError, ComponentAddressError
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
                 reraise_runtime_exceptions: bool = True,
                 capture_termination_exceptions: bool = True,
                 log_to_osc: bool = True,
                 osc_log_address: Optional[str] = None,
                 *args, **kwargs):
        super().__init__(parse_parenthesis_as_list=False,
                         discard_duplicate_args=discard_duplicate_args,
                         *args, **kwargs)
        self.logger = logging.getLogger(__name__)

        self.recv_port: int = recv_port
        self.send_port: int = send_port
        self.ip: str = ip
        self.default_address: str = default_address
        self.reraise_exceptions: bool = reraise_runtime_exceptions
        self.capture_termination_exceptions: bool = capture_termination_exceptions

        self._sender: OscSender = OscSender(ip, send_port)

        self.osc_log_handler: Optional[OscLogForwarder] = None
        self.osc_log_address: Optional[str] = None
        if log_to_osc:
            self.osc_log_address = default_address if osc_log_address is None else osc_log_address
            if not self.is_valid_osc_address(self.osc_log_address):
                raise ConfigurationError(f"'{self.osc_log_address}' is not a valid OSC address")

        self._server: Optional[AsyncIOOSCUDPServer] = None

        self._async_targets: List[Callable[[], Awaitable[None]]] = []

        self.__running: bool = False

    @staticmethod
    def default_log_config():
        """ Call this at the beginning of _main_loop in each new multiprocessing.Process """
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s]: %(message)s')

    @abstractmethod
    async def _main_loop(self):
        """ Main loop function """

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
        if not self.capture_termination_exceptions:
            asyncio.run(self._run())

        else:
            try:
                asyncio.run(self._run())
            except OSError as e:
                self.logger.critical(f"{str(e)}. Couldn't start '{self.__class__.__name__}'")
                self.stop()
            except KeyboardInterrupt:
                self.logger.critical(f"Terminating due to keyboard interrupt (SIGINT)")
                self.stop()

    def stop(self) -> None:
        self.__running = False

    def add_async_target(self, func: Callable[[], Awaitable[None]]) -> None:
        """ Add additional async functions to call continuously running. Each function needs their own loop
        and should utilize `self.running` ideally. """
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

    def set_log_level(self, logging_level: int):
        if self.osc_log_handler is None:
            raise ConfigurationError("object does not have OSC logging enabled")

        self.osc_log_handler.set_log_level(logging_level=logging_level)

    @property
    def running(self):
        """ Note: Should be used to control main loop """
        return self.__running

    async def _run(self) -> None:
        """ raises: OSError is server already is in use """
        self.__running = True

        if self.osc_log_address:
            self.osc_log_handler = OscLogForwarder(self._sender, self.osc_log_address)
            self.logger.addHandler(self.osc_log_handler)
        osc_dispatcher: Dispatcher = Dispatcher()
        # python-osc will regexp-replace '*' with '[^/]*?/*', resulting in matches between /some_address and
        # /some_address2 even when the goal is to match only /some_address/some_child, hence the additional regex
        osc_dispatcher.map(f"{self.default_address}($|/*)", self.__process_osc)
        osc_dispatcher.set_default_handler(self.__unmatched_osc)
        self._server: AsyncIOOSCUDPServer = AsyncIOOSCUDPServer((self.ip, self.recv_port),
                                                                osc_dispatcher, asyncio.get_event_loop())
        transport, protocol = await self._server.create_serve_endpoint()
        await asyncio.gather(self._main_loop(), *[f() for f in self._async_targets])
        transport.close()

    def __process_osc(self, address: str, *args):
        args_str: str = MaxFormatter.format_as_string(*args)
        try:
            self.call(args_str, prepend_args=[address])

        # Called with wrong number of arguments, with duplicate arguments or calling function that doesn't exist
        except MaxOscError as e:
            self.logger.error(e)
            self.logger.debug(repr(e))

        # Any other exception
        except Exception as e:
            self.logger.error(e)
            self.logger.debug(repr(e))
            if self.reraise_exceptions:
                raise

    def __unmatched_osc(self, address: str, *_args, **_kwargs) -> None:
        self.logger.warning(f"The address '{address}' does not exist.")

    @staticmethod
    def parse_ip(ip: str) -> str:
        """ raises: ValuError if ip is invalid """
        ipaddress.ip_address(ip)
        return ip

    @staticmethod
    def path_to_osc_address(component_path: List[str]) -> str:
        return "/" + "/".join(component_path)

    @staticmethod
    def osc_address_to_path(osc_address: str) -> List[str]:
        if osc_address.startswith("/"):
            return osc_address.split("/")[1:]
        return osc_address.split()

    @staticmethod
    def max_address_to_path(max_address: str) -> List[str]:
        """ max address on the form `parent::child::{..}::parameter`"""
        return max_address.split(sep="::")

    @staticmethod
    def is_valid_osc_address(osc_address: str) -> bool:
        return osc_address.startswith("/")


# TODO: Expand constructor to args of AsyncOsc once implementation has matured
class AsyncOscMPC(AsyncOsc, multiprocessing.Process, ABC):
    def __init__(self, *args, **kwargs):
        # It's critical that multiprocessing.Process is initialized without any arguments
        # and that `AsyncOscWithStatus` is declared first in the __mro__
        AsyncOsc.__init__(self, *args, **kwargs)
        multiprocessing.Process.__init__(self)


class AsyncOscWithStatus(AsyncOsc, ABC):
    STATUS_OSC_ADDRESS = "status"

    def __init__(self,
                 recv_port: int,
                 send_port: int,
                 ip: str,
                 default_address: str,
                 discard_duplicate_args: bool = False,
                 reraise_runtime_exceptions: bool = True,
                 capture_termination_exceptions: bool = True,
                 status_interval_s: float = 0.5,
                 *args, **kwargs):
        super().__init__(recv_port=recv_port,
                         send_port=send_port,
                         ip=ip,
                         default_address=default_address,
                         discard_duplicate_args=discard_duplicate_args,
                         reraise_runtime_exceptions=reraise_runtime_exceptions,
                         capture_termination_exceptions=capture_termination_exceptions,
                         *args, **kwargs)
        self.status_interval_s: float = status_interval_s

        self._map: Dict[str, Tuple[Component, str]] = {}
        self.add_async_target(self.heartbeat_loop)

    async def heartbeat_loop(self) -> None:
        while self.running:
            self.send_status_to_all(Status.READY)
            await asyncio.sleep(self.status_interval_s)

        # When correctly terminated, send termination status
        self.send_status_to_all(Status.TERMINATED)

    def register_osc_component(self,
                               osc_address: str,
                               osc_status_address: str,
                               component: Component,
                               override: bool = False) -> None:
        """ raises: ComponentAddressError if component exists and override is False """
        if osc_address in self._map and not override:
            raise ComponentAddressError(f"A component ({self._map[osc_address][0].name}) is already "
                                        f"registered for '{osc_address}'")

        self._map[osc_address] = component, osc_status_address

    def deregister_osc_component(self, osc_address: str) -> None:
        if osc_address not in self._map:
            raise ComponentAddressError(f"No component registered for '{osc_address}'")

        del self._map[osc_address]
        self.send_status(osc_address, Status.TERMINATED)

    def send_status(self, status_address: str, status: Status) -> None:
        self.send(status, address=status_address)

    def send_status_to_all(self, status: Status) -> None:
        for address in self.status_addresses:
            self.send_status(address, status)

    def component_at(self, osc_address: str) -> Component:
        """ raises ComponentAddressError if component doesn't exist """
        try:
            return self._map[osc_address][0]
        except KeyError:
            raise ComponentAddressError(f"No component registered for '{osc_address}'")

    @property
    def addresses(self) -> List[str]:
        return list(self._map.keys())

    @property
    def status_addresses(self) -> List[str]:
        return [status_address for _, status_address in self._map.values()]


# TODO: Expand constructor to args of AsyncOscWithStatus once implementation has matured
class AsyncOscMPCWithStatus(AsyncOscWithStatus, multiprocessing.Process, ABC):
    def __init__(self, *args, **kwargs):
        # It's critical that multiprocessing.Process is initialized without any arguments
        # and that `AsyncOscWithStatus` is declared first in the __mro__
        AsyncOscWithStatus.__init__(self, *args, **kwargs)
        multiprocessing.Process.__init__(self)
