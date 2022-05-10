from typing import List, Any, Tuple, Dict, Union

from merge.io.parameter import Parameter


class Component:
    """ Interface for addressing `Parameters` in a hierarchy dynamically over OSC. This class is also used to check
        status of components"""

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name: str = name

    def set_parameter(self, parameter_path: List[str], value: Any) -> None:
        """ raises: ParameterError if trying to set existing parameter with an invalid value
                    InputError if no parameter exists at `parameter_path`"""

    def get_parameter(self, parameter_path: List[str]) -> Parameter:
        """ raises: InputError if no parameter exists at `parameter_path` """

    def get_parameters(self) -> List[Tuple[List[str], Parameter]]:
        """ returns a list of parameters with their corresponding pathspecs """
        pass

    def get_components(self) -> List[Tuple[List[str], 'Component']]:
        """ returns a list of components with their corresponding pathspecs """
        pass

    def update_components(self) -> None:
        """ update pre-computed `_parameter_tree` when adding/removing a component to the hierarchy """
