"""
This module provides access to utility functions that are used universally across the application.

Features:
- Import of universal utility functions for local development.
- Definition of publicly accessible objects for this module.
"""

# Import all utility functions from the universal_utility_functions module
from .universal_utility_functions import *

# Define the list of public objects for this module
__all__ = [
    "get_custom_logger",  # Custom logger function available for external use
]  # __all__ is a list of attribute names that are considered public in this module