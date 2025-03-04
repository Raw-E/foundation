"""
This module serves as an import aggregator for local development package components.

Features:
- Imports all components from the version 1 subpackage.
- Defines the `__all__` list to control what is exported when `from module import *` is used.
"""

# # Import all components from the version 1 subpackage
# from .v1 import *  # Imports all the available components from the 'v1' subpackage, making them accessible in this module.

# # Define __all__ list to specify what is exported when using 'from module import *'
# __all__ = []  # An empty list indicating that nothing is explicitly exported when using 'from module import *', unless defined.

from typing import Literal, Dict, Any, List
import importlib
import sys

VersionType = Literal["v1", "v2"]  # Add more versions as needed

__version__: VersionType = "v1"
__all__: List[str] = []  # This will be populated dynamically

def set_version(version: VersionType) -> None:
    global __version__, __all__
    __version__ = version
    _update_all()

def get_version() -> VersionType:
    return __version__

def _update_all() -> None:
    global __all__
    module = importlib.import_module(f".{__version__}", package="foundation")
    if hasattr(module, '__all__'):
        __all__ = module.__all__
    else:
        __all__ = [name for name in dir(module) if not name.startswith('_')]
    
    # Update the current module's attributes
    for name in __all__:
        setattr(sys.modules[__name__], name, getattr(module, name))

# Initialize __all__ and attributes
_update_all()

# Expose version-related functions
use_version = set_version
get_current_version = get_version

# IDEA: Add a function to list available components for the current version
def list_components() -> List[str]:
    return __all__