"""
This module serves as the initialization file for the python_file_templates package.

It defines package-level imports, exports, and metadata to control what is exposed
to users of this package.
"""

from .general_comparison_utilities import *

# Package metadata
__version__: str = "0.1.0"
__author__: str = "Your Name"
__email__: str = "your.email@example.com"

# Define what should be exposed when using 'from package import *'
__all__: List[str] = [
    "parts_match_in_order",
]

# IDEA: Consider adding package-level constants or configuration here
# IDEA: You could add a get_version() function to handle semantic versioning
# IDEA: Consider adding a setup() function for any package initialization needs

# You can also import and expose specific items from submodules
# Example:
# from .submodule import SomeClass
# from .helpers import utility_function