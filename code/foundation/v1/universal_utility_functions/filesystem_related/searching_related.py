"""
File: searching_related.py

This module contains utilities for searching and discovering classes and files within a filesystem.

Functions:
   - get_subclasses_in_folder(folder_path, base_class, classes_to_omit): Find all subclasses of a specified base class in a given folder, excluding specified class names.

Usage:
   from searching_related import get_subclasses_in_folder

   # Example usage of get_subclasses_in_folder
   from some_module import BaseClass
   subclasses = get_subclasses_in_folder('/path/to/folder', BaseClass, ['ClassToOmit'])
   print(subclasses)

Dependencies:
   - os
   - importlib
   - inspect
   - typing

For detailed documentation, see the individual function docstrings.
"""


# Standard library imports
import os
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, Type, List, Optional

# Third-party imports
# None for this module

# Local application imports
from ..logging_related.general_logging_utilities import get_custom_logger

logger = get_custom_logger()

def get_subclasses_in_folder(folder_path: str, base_class: Type, classes_to_omit: List[str] = None) -> Dict[str, Type]:
    """
    Find all subclasses of the specified base_class in the given folder, excluding specified class names.

    Args:
    ----
        folder_path (str): The path to the folder to search in.
        base_class (Type): The base class to look for subclasses of.
        classes_to_omit (List[str], optional): List of class names to exclude from the results. Defaults to None.

    Returns:
    -------
        Dict[str, Type]: A dictionary of discovered subclasses.

    Example:
    -------
        >>> from some_module import BaseClass
        >>> subclasses = get_subclasses_in_folder('/path/to/folder', BaseClass, ['ClassToOmit'])
        >>> print(subclasses)
        {'SubClass1': <class 'module.SubClass1'>, 'SubClass2': <class 'module.SubClass2'>}
    """
    logger.debug(f"Searching for subclasses of {base_class.__name__} in {folder_path}")

    subclasses = {}
    classes_to_omit = classes_to_omit or []

    logger.info("about to start importing modules")

    def import_module(file_path: str) -> None:
        try:
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, base_class) and 
                    obj != base_class and 
                    name not in classes_to_omit):
                    subclasses[name] = obj
                    logger.debug(f"Found subclass: {name}")
        except Exception as e:
            logger.error(f"Error importing module {file_path}: {str(e)}")

    if not os.path.exists(folder_path):
        logger.error(f"Folder not found: {folder_path}")
        return subclasses

    for root, _, files in os.walk(folder_path):
        logger.debug(f"Searching in folder: {root}")
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                logger.debug(f"Examining file: {file}")
                file_path = os.path.join(root, file)
                import_module(file_path)

    logger.info(f"Found {len(subclasses)} subclasses of {base_class.__name__}")
    return subclasses

def find_path_up_to_boundary(
    start_path: Path, 
    target_name: str, 
    search_boundary_path: Optional[Path] = Path.home() / "Desktop"
) -> Optional[Path]:
    """
    Find a file or directory by searching upwards through parent directories.

    Args:
        start_path (Path): Starting path for the search
        target_name (str): Name of the file or directory to find
        search_boundary_path (Optional[Path]): Upper boundary directory path limit for the search (default: Desktop)

    Returns:
        Optional[Path]: Path to the found target or None if not found
    """
    # Resolve paths once at the start
    current_dir: Path = start_path.resolve()
    search_boundary_path = search_boundary_path.resolve()
    
    # Handle file path input
    if current_dir.is_file():
        current_dir = current_dir.parent
    
    try:
        while current_dir.is_relative_to(search_boundary_path):
            target_path: Path = current_dir / target_name
            if target_path.exists():
                logger.debug(f"Found {target_name} at: {target_path}")
                return target_path
            
            # Stop if we've reached the root directory
            if current_dir == current_dir.parent:
                break
                
            current_dir = current_dir.parent
            
    except Exception as e:
        logger.error(f"Error while searching for {target_name}: {e}")
        return None

    logger.debug(f"{target_name} not found up to {search_boundary_path} directory")
    return None



# TODO: Consider adding more search-related utility functions
# IDEA: Implement a function to search for files with specific content
