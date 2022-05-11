import collections.abc
from typing import List, Any, Tuple, Iterable, Dict

from merge.io.addressable import Addressable
from merge.io.parameter import Parameter
from merge.main.exceptions import InputError


class Component(Addressable):
    """ Interface for addressing `Parameters` in a hierarchy dynamically over OSC. It is able to locate all components
        and parameters stored inside other `Component`s, and on the first level of lists and dictionaries

        It's possible to create several `Component`s with the same name, potential issues with duplicate names must be
        handled manually.
    """

    def __init__(self, name: str,
                 search_lists: bool = False,
                 search_dictionary_keys: bool = False,
                 search_dictionary_values: bool = False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name: str = name

        self.search_lists: bool = search_lists
        self.search_dictionary_keys: bool = search_dictionary_keys
        self.search_dictionary_values: bool = search_dictionary_values

    def set_parameter(self, parameter_path: List[str], value: Any) -> None:
        """ raises: ParameterError if trying to set existing parameter with an invalid value
                    InputError if no parameter exists at `parameter_path`"""
        # TODO: If needed, this can be heavily optimized, rather than parsing the entire tree at each call, either by
        #       precomputing the tree or by DFS-searching the tree
        self.get_parameter(parameter_path).value = value

    def get_parameter(self, parameter_path: List[str]) -> Parameter:
        """ raises: InputError if no parameter exists at `parameter_path` """
        try:
            parameters: List[Tuple[List[str], Parameter]] = self.get_parameters()
            parameter_dict: Dict[Tuple[str], Parameter] = {tuple(address): param for (address, param) in parameters}
            return parameter_dict[tuple(parameter_path)]
        except KeyError:
            raise InputError(f"parameter '{'::'.join(parameter_path)}' does not exists")

    def get_parameters(self) -> List[Tuple[List[str], Parameter]]:
        """ returns a list of parameters with their corresponding pathspecs """
        return [(address, obj)
                for (address, obj) in self._get_addressables([])
                if isinstance(obj, Parameter)]

    def get_components(self) -> List[Tuple[List[str], 'Component']]:
        """ returns a list of components with their corresponding pathspecs """
        return [(address, obj)
                for (address, obj) in self._get_addressables([])
                if isinstance(obj, Component)]

    def component_exists(self, component_path: List[str]) -> bool:
        component_paths: List[List[str]] = [path for (path, _) in self.get_components()]
        return component_path in component_paths

    def _get_addressables(self, parent_names: List[str]) -> List[Tuple[List[str], Addressable]]:
        addressables: List[Tuple[List[str], Addressable]] = []
        for _, item in self.__dict__.items():  # type: Any
            if isinstance(item, Component):
                addressables.append((parent_names + [item.name], item))
                addressables.extend(item._get_addressables(parent_names=parent_names + [item.name]))

            elif isinstance(item, Parameter):
                addressables.append((parent_names + [item.name], item))

            elif isinstance(item, collections.abc.Mapping):
                if self.search_dictionary_keys:
                    addressables.extend(self._search_iterable(parent_names, item.keys()))
                if self.search_dictionary_values:
                    addressables.extend(self._search_iterable(parent_names, item.values()))

            elif self.search_lists and isinstance(item, collections.abc.Iterable):
                addressables.extend(self._search_iterable(parent_names, item))

        return addressables

    @staticmethod
    def _search_iterable(parent_names: List[str], iterable: Iterable) -> List[Tuple[List[str], Addressable]]:
        addressables: List[Tuple[List[str], Addressable]] = []
        for item in iterable:
            if isinstance(item, Component):
                addressables.append((parent_names + [item.name], item))
                addressables.extend(item._get_addressables(parent_names=parent_names + [item.name]))
            elif isinstance(item, Parameter):
                addressables.append((parent_names + [item.name], item))
            # do not search iterables recursively
        return addressables
