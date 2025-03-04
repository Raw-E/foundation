from abc import ABC
from typing import Any, Optional

from ..universal_utility_functions import get_custom_logger

logger = get_custom_logger()

"""
Questions:
- What should I consider to be a component?
- Should this code be used for something else?
- Should I have classes that inherit from a class like this?
"""

class Component(ABC):
    should_register_on_instance_creation: bool = False

    def __init__(self, should_register: Optional[bool] = None, registry: Optional[Any] = None) -> None:
        self._register_if_needed(should_register, registry)

    def _register_if_needed(self, should_register: Optional[bool], registry: Optional[Any]) -> None:
        if (should_register if should_register is not None else self.should_register_on_instance_creation):
            self._registry = registry or self._get_default_registry()
            self._register()

    def _get_default_registry(self) -> Any:
        from .universal_components.registry import Registry
        return Registry

    @property
    def is_registered(self) -> bool:
        return getattr(self, '_id', None) is not None

    @property
    def id(self) -> Optional[str]:
        return getattr(self, '_id', None)
    
    def _register(self) -> None:
        if self._id is not None:
            logger.debug(f"Component already registered with ID: {self._id}")

        self._id = self._registry.register_data(alias=self.__class__.__name__, data=self)
        logger.debug(f"Component registered with ID: {self._id}")