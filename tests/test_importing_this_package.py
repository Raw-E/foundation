# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for test_importing_this_package.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
import importlib
from importlib.util import find_spec

# Third-Party Imports
import pytest


# Main Functions
def test_importing_this_package():
    spec = find_spec("foundation")
    assert spec is not None, "Package 'foundation' not found!"

    try:
        importlib.import_module("foundation")
    except ImportError as e:
        pytest.fail(f"Failed to import 'foundation' package: {e}")
