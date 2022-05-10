import functools
from typing import TypeVar, Generic, Optional, Callable, List

from merge.io.param_utils import MaxType, ParameterRange
from merge.main.exceptions import ParameterError, ConfigurationError

T = TypeVar('T')


class Parameter(Generic[T]):
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
        self.type_info: Optional[MaxType] = type_info
        self.param_range: Optional[ParameterRange] = param_range
        self.description: Optional[str] = description
        self.on_parameter_change: Optional[Callable[[T], None]] = on_parameter_change

        def compose(f, g):
            return lambda x: f(g(x))

        input_validation: List[Callable[[T], T]] = []
        if check_range:
            if self.param_range is None:
                raise ConfigurationError("no range specification was provided, checking range is not possible")
            input_validation.append(self._in_range)

        if check_type:
            if self.type_info is None:
                raise ConfigurationError("no type specification was provided, checking type is not possible")
            input_validation.append(self._valid_type)

        self.validate_input: Callable[[T], T] = functools.reduce(compose, input_validation)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: T):
        """ raises: ParameterError if outside range or of invalid type, assuming range and/or type checks are enabled"""
        self.validate_input(value)
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
