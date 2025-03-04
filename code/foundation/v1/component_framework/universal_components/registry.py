"""
This module provides a generic Registry class that allows managing items by unique IDs.

Features:
- Register, retrieve, and remove data by ID or type.
- Generate unique IDs for new data entries.
- Singleton pattern to ensure a single instance of the registry.
"""

from collections import defaultdict
import uuid
from typing import Any, Dict, List, Optional, Union, Tuple

from ...universal_utility_functions import get_custom_logger
from ..component import Component

# Type alias for registry data
RegistryData = Dict[str, Any]

# Initialize logger
logger = get_custom_logger()


class Registry(Component):
    """
    A generic registry class to manage items identified by IDs.
    Inherits from Component to combine component functionality with registry management.

    Attributes:
        _stored_data (Dict[str, Dict[str, Any]]): Central storage for registered data.
        DEFAULT_TYPE (str): The default type assigned to data when no type is specified.

    Methods:
        _generate_unique_id(): Generates a unique ID for new entries.
        register_data(): Registers new data in the registry.
        get_data_by_id(): Retrieves data by its ID.
        get_data_by_type(): Retrieves all data of a specific type.
        get_all_data(): Returns all data in the registry.
        remove_data_by_id(): Removes data by its ID.
        remove_data_by_type(): Removes all data of a specific type.
    """

    _stored_data: Dict[str, Dict[str, Any]] = {}
    DEFAULT_TYPE = "default"

    @classmethod
    def _generate_unique_id(cls) -> str:
        """Generates a unique ID that does not exist in the registry."""
        while True:
            unique_id = str(uuid.uuid4())
            if unique_id not in cls._stored_data:
                return unique_id

    @classmethod
    def register_data(cls, data_id: Optional[str] = None, data_type: Optional[str] = None, alias: Optional[str] = None, data: Any = None) -> Tuple[str, str]:
        """
        Registers new data in the registry, updating if ID already exists.
        
        Args:
            data_id (Optional[str]): The ID for the data. If None, a unique ID is generated.
            data_type (Optional[str]): The type of the data.
            word_identifier (Optional[str]): A unique word identifier for the data.
            data (Any): The data to be stored.

        Returns:
            Tuple[str, str]: A tuple containing the data_id and word_identifier.
        """
        if data_id is None:
            data_id = cls._generate_unique_id()
        if data_id in cls._stored_data:
            logger.warning(f"Data with ID {data_id} already exists. Updating the existing data.")

        if alias is None:
            alias = f"item_{data_id[:8]}"  # Generate a default word identifier if not provided

        entry = {
            "alias": alias,
            "data": data
        }
        if data_type and data_type != cls.DEFAULT_TYPE:
            entry["dataType"] = data_type

        cls._stored_data[data_id] = entry
        
        return data_id, alias

    @classmethod
    def get_data_by_id(cls, id: str) -> Optional[Any]:
        """Retrieves and logs data by its unique ID."""
        entry = cls._stored_data.get(id)
        if entry is None:
            logger.debug(f"No data found in the registry for ID: {id}")
            return None
        else:
            logger.debug(f"Data retrieved from the registry for ID: {id}")
            return entry["data"]

    @classmethod
    def get_data_by_alias(cls, alias: str) -> Optional[Tuple[str, Any]]:
        """
        Retrieves data by its word identifier.

        Args:
            word_identifier (str): The word identifier to search for.

        Returns:
            Optional[Tuple[str, Any]]: A tuple containing the ID and data if found, otherwise None.
        """
        for entry in cls._stored_data.values():
            if entry["alias"] == alias:
                return entry["data"]
        logger.debug(f"No data found in the registry for alias: {alias}")
        return None


    @classmethod
    def get_data_by_type(cls, data_type: str = DEFAULT_TYPE) -> List[Dict[str, Any]]:
        """Fetches all data entries matching a specific type."""
        return [
            {"id": id, "wordIdentifier": entry["wordIdentifier"], "data": entry["data"]}
            for id, entry in cls._stored_data.items()
            if entry.get("dataType", cls.DEFAULT_TYPE) == data_type
        ]

    @classmethod
    def get_all_data(cls) -> List[Dict[str, Any]]:
        """Returns all data entries stored in the registry."""
        return [
            {"id": id, "wordIdentifier": entry["wordIdentifier"], "data": entry["data"]}
            for id, entry in cls._stored_data.items()
        ]

    @classmethod
    def remove_data_by_id(cls, id: str) -> bool:
        """Attempts to remove data by ID, logging the outcome."""
        if id in cls._stored_data:
            del cls._stored_data[id]
            logger.debug(f"Data removed from the registry for ID: {id}")
            return True
        else:
            logger.debug(f"No data found in the registry for ID: {id} to remove.")
            return False

    @classmethod
    def remove_data_by_type(cls, data_type: str) -> int:
        """Removes all data entries of a specific type and logs the count."""
        ids_to_remove = [
            id for id, entry in cls._stored_data.items()
            if entry.get("dataType", cls.DEFAULT_TYPE) == data_type
        ]
        removed_count = len(ids_to_remove)
        for id in ids_to_remove:
            del cls._stored_data[id]
            logger.debug(f"Data removed from the registry for ID: {id}, Type: {data_type}")

        logger.debug(f"Total {removed_count} entries of type '{data_type}' removed from the registry.")
        return removed_count

    @classmethod
    def bulk_register_data(cls, data_list: List[Dict[str, Any]]) -> List[str]:
        """Registers multiple data entries and returns their IDs."""
        ids = []
        for data in data_list:
            data_id = data.get("data_id")
            data_type = data.get("data_type")
            data_content = {k: v for k, v in data.items() if k not in {"data_id", "data_type"}}
            ids.append(cls.register_data(data_id, data_type, **data_content))
        return ids

    @classmethod
    def bulk_remove_data_by_ids(cls, ids: List[str]) -> int:
        """Removes multiple data entries by their IDs and returns the count of removed entries."""
        removed_count = 0
        for id in ids:
            if cls.remove_data_by_id(id):
                removed_count += 1
        return removed_count