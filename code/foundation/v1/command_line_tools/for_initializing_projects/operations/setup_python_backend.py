"""Module: setup_python_backend.py

This module contains the SetupPythonBackend class, which is responsible for setting up
a new Python backend project.

Classes:
    - SetupPythonBackend: Handles the setup process for a new Python backend project.

Usage:
    from setup_python_backend import SetupPythonBackend

    # Example usage of SetupPythonBackend
    setup = SetupPythonBackend("my_new_project")
    new_project_dir = await setup.execute()

Dependencies:
    - os
    - typing
    - ...operation_framework.operation
    - ...universal_utility_functions.filesystem_related.general_filesystem_utilities

For detailed documentation, see the individual class and method docstrings.
"""

# Standard library imports
import os
from typing import Any

# Local application imports
from ....operation_framework.operation import Operation
from ....universal_utility_functions.filesystem_related.general_filesystem_utilities import copy_file_or_directory

# Constants
PYTHON_BACKEND_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "python_backend_template")

class SetupPythonBackend(Operation):
    """Class to set up a new Python backend project.

    This class inherits from the Operation class and provides functionality
    to create a new Python backend project by copying template files to a
    specified location.

    Attributes
    ----------
        project_name (str): The name of the new project to be created.

    Methods
    -------
        execute(*args: Any, **kwargs: Any) -> str:
            Executes the backend project setup process.

    Usage:
        setup = SetupPythonBackend("my_new_project")
        new_project_dir = await setup.execute()

    """

    def __init__(self, project_directory: str):
        """Initialize the SetupPythonBackend instance.

        Args:
        ----
            project_name (str): The name of the new project to be created.

        """
        super().__init__()
        self.project_directory = project_directory

    async def execute(self, *args: Any, **kwargs: Any) -> str:
        """Execute the backend project setup process.

        This method creates a new directory for the project on the user's desktop
        and copies the backend template files into it.

        Args:
        ----
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
        -------
            str: The path to the newly created project directory.

        TODO: Consider adding error handling for file operations.
        IDEA: Implement a configuration file for customizing the setup process.

        """
        # Copy backend template files to the new project directory
        copy_file_or_directory(PYTHON_BACKEND_TEMPLATE_DIR, self.project_directory)


# Exception classes
# Add any custom exception classes here if needed
