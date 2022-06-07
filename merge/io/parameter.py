from typing import TypeVar, Generic, Optional, Callable, List, Union

from merge.io.addressable import Addressable
from merge.io.param_utils import MaxType, ParameterRange
from merge.main.exceptions import ParameterError, ConfigurationError

T = TypeVar('T')


class Parameter(Generic[T], Addressable):
    """ Class for setting parameters that should be accessible over OSC.

        Note that the `on_parameter_change` can be used if updating the given parameter should change additional values
        elsewhere, for example:
        >>> class SomeClass:
        >>>     def __init__(self):
        >>>         self.a: float
        >>>         self.b: Parameter[int] = Parameter("b", 0, on_parameter_change=self.calculate_a)
        >>>
        >>>     def calculate_a(self, b):
        >>>         self.a = b / 2
    """

    def __init__(self,
                 name: str,
                 default_value: T,
                 type_info: Optional[MaxType] = None,
                 param_range: Optional[ParameterRange] = None,
                 description: Optional[str] = None,
                 check_range: bool = False,
                 check_type: bool = False,
                 on_parameter_change: Optional[Callable[[T], None]] = None):
        self.name = name
        self._value: T = default_value
        self._default_value: T = default_value  # Only used to inform renderer about defaults
        self.type_info: Optional[MaxType] = type_info
        self.param_range: Optional[ParameterRange] = param_range
        self.description: Optional[str] = description
        self.on_parameter_change: Optional[Callable[[T], None]] = on_parameter_change

        if check_range and self.param_range is None:
            raise ConfigurationError("no range specification was provided, checking range is not possible")

        if check_type and self.type_info is None:
            raise ConfigurationError("no type specification was provided, checking type is not possible")

        self.check_range: bool = check_range
        self.check_type: bool = check_type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: T):
        """ raises: ParameterError if outside range or of invalid type, assuming range and/or type checks are enabled"""
        if self.check_range:
            self._in_range(value)

        if self.check_type:
            self._valid_type(value)

        self._value = value
        if self.on_parameter_change is not None:
            self.on_parameter_change(value)

    def _in_range(self, value: T) -> T:
        if value not in self.param_range:
            raise ParameterError(f"value {value} is out of range for parameter '{self.name}'")
        return value

    def _valid_type(self, value: T) -> T:
        if not self.type_info.matches(value):
            raise ParameterError(f"value {value} does not match type '{self.type_info.renderer_info()}'")
        return value

    def renderer_info(self) -> List[Union[int, float, str]]:
        info: List[Union[int, float, str]] = [self.name,
                                              self.value,
                                              self._default_value]
        if self.type_info is not None:
            info.append(self.type_info.renderer_info())

        if self.param_range is not None:
            info.append(self.param_range.renderer_info())

        if self.description is not None:
            info.append(self.description)

        return info
