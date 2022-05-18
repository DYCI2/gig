# TODO: Remove
# from typing import Dict, List, Tuple
#
# from merge.io.component import Component
# from merge.main.exceptions import ComponentAddressError
#
#
# class OscRemoteManager:
#
#     def __init__(self):
#         self._map: Dict[str, Tuple[Component, str]] = {}
#
#     def register_component(self, osc_address: str,
#                            osc_status_address: str,
#                            component: Component,
#                            override: bool = False) -> None:
#         """ raises: ComponentAddressError if component exists and override is False """
#         if osc_address in self._map and not override:
#             raise ComponentAddressError(f"A component ({self._map[osc_address][0].name}) is already "
#                                         f"registered for '{osc_address}'")
#
#         self._map[osc_address] = component, osc_status_address
#
#     def deregister_component(self, osc_address: str) -> None:
#         if osc_address not in self._map:
#             raise ComponentAddressError(f"No component registered for '{osc_address}'")
#
#         del self._map[osc_address]
#
#     def addresses(self) -> List[str]:
#         return list(self._map.keys())
#
#     def status_addresses(self) -> List[str]:
#         return [status_address for _, status_address in self._map.values()]
