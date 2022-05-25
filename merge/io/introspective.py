import collections.abc
import inspect
import sys
from types import ModuleType
from typing import Type, Any, Optional, List, Union, Dict, TypeVar

from merge.main.exceptions import ConfigurationError

T = TypeVar('T')


class Introspective:
    @staticmethod
    def introspect(base_class: Type[T],
                   modules: Optional[Union[ModuleType, List[ModuleType]]] = None,
                   include_abstract: bool = False) -> Dict[str, Type[T]]:
        """ Returns all classes inheriting from base class in the given module(s)
            raises: ConfigurationError if multiple classes with the same name exists """
        if modules is None:
            modules: List[ModuleType] = [sys.modules[base_class.__module__]]
        else:
            modules: List[ModuleType] = [modules] if not isinstance(modules, collections.abc.Iterable) else modules

        all_classes: List[Dict[str, T]] = []
        for module in modules:
            all_classes.append(Introspective._introspect_module(base_class, module, include_abstract))

        return Introspective._merge_dicts(all_classes)

    ##############################################################################################
    # PRIVATE
    ##############################################################################################

    @staticmethod
    def _introspect_module(base_class: Type[T],
                           module: ModuleType,
                           include_abstract: bool) -> Dict[str, Type[T]]:
        classes: Dict[str, Any] = dict(
            inspect.getmembers(module, lambda m: Introspective._is_subclass(base_class, m, include_abstract))
        )
        return {k.lower(): v for (k, v) in classes.items()}

    @staticmethod
    def _is_subclass(base_class: Type[T], candidate_class: Type[T], include_abstract: bool) -> bool:
        return inspect.isclass(candidate_class) \
               and issubclass(candidate_class, base_class) \
               and (include_abstract or not inspect.isabstract(candidate_class))

    @staticmethod
    def _merge_dicts(all_classes: List[Dict[str, T]]) -> Dict[str, T]:
        """ raises ConfigurationError if multiple classes with the same name exists """
        combined: Dict[str, T]= {}
        for class_dict in all_classes:
            for key, value in class_dict.items():
                if key in combined:
                    if combined[key] != value:
                        raise ConfigurationError(f"found multiple classes with the key '{key}'")
                    # else: ignore, the entry is already in the dict
                else:
                    combined[key] = value

        return dict(collections.ChainMap(*all_classes))
