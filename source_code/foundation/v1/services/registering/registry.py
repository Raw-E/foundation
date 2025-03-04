"""
This module provides a registry for storing and retrieving data.
"""

from abc import ABC
from typing import Any, Dict, Optional, Union
import uuid

from ..logging.custom_logger import CustomLogger

# Initialize a logger instance for capturing info and error messages.
logger = CustomLogger()


class Registerable(ABC):
    should_register_by_default: bool = True

    def __init__(self, should_register: Optional[bool] = None, registry: Optional[Any] = None) -> None:
        self._registry = registry or self._get_default_registry()
        self._id = None
        self._register_on_creation_if_needed(should_register)

    def register(self) -> str:
        if self.is_registered:
            raise RuntimeError(f"Component already registered with ID: {self.id}")

        self._id = self._registry.register_data(alias=self.__class__.__name__, data=self)
        logger.info(f"Component registered with ID: {self._id}")

        return self._id

    def _register_on_creation_if_needed(self, should_register: Optional[bool]) -> None:
        should_perform_registration = (
            should_register if should_register is not None else self.should_register_by_default
        )

        if should_perform_registration:
            self.register()

    def _get_default_registry(self) -> Any:
        return Registry

    @property
    def is_registered(self) -> bool:
        return getattr(self, "_id", None) is not None

    @property
    def id(self) -> Optional[str]:
        return getattr(self, "_id", None)


class Registry:
    """
    A registry for storing and retrieving data.

    This class provides a way to store data with unique identifiers and retrieve it later.
    It supports both direct data storage and aliased data storage.
    """

    _data: Dict[str, Any] = {}
    _aliases: Dict[str, str] = {}

    @classmethod
    def register_data(cls, data: Any, alias: Optional[str] = None) -> str:
        """
        Register data in the registry.

        Args:
            data: The data to register
            alias: Optional alias for the data

        Returns:
            The ID of the registered data
        """
        data_id = str(uuid.uuid4())
        cls._data[data_id] = data
        if alias:
            cls._aliases[alias] = data_id
            logger.info(f"Registered data with ID {data_id} and alias {alias}")
        else:
            logger.info(f"Registered data with ID {data_id}")
        return data_id

    @classmethod
    def get_data(cls, identifier: Union[str, uuid.UUID]) -> Any:
        """
        Get data from the registry.

        Args:
            identifier: The ID or alias of the data to retrieve

        Returns:
            The retrieved data

        Raises:
            KeyError: If the data is not found
        """
        data_id = str(identifier)
        if data_id in cls._aliases:
            data_id = cls._aliases[data_id]
        return cls._data[data_id]

    @classmethod
    def clear(cls) -> None:
        """Clear all data from the registry."""
        cls._data.clear()
        cls._aliases.clear()
        logger.info("Registry cleared")
