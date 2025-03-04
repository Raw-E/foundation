"""Module: setup_python_project.py

This module provides functionality for setting up new Python projects,
including both packages and backend applications.

Classes:
    - SetupPythonProject: Main class to set up a new Python project.

Usage:
    from dev_pytopia.v1.command_line_tools.automatic_package_creator.setup_new_python_project import SetupNewPythonProject

    # Example usage for setting up a new Python package
    setup = SetupNewPythonProject("my_new_package")
    await setup.execute()

    # Example usage for setting up a new Python backend
    setup_backend = SetupNewPythonProject("my_new_backend", is_backend=True)
    await setup_backend.execute()

Dependencies:
    - dev_pytopia.v1.operation_framework.operation
    - .setup_python_backend
    - .setup_python_package

For detailed documentation, see the individual class and method docstrings.
"""

# Standard library imports
import os
from typing import Any

# Local application imports
from ....operation_framework.operation import Operation
from .setup_python_backend import SetupPythonBackend
from .setup_python_package import SetupPythonPackage


class SetupPythonProject(Operation):
    """Main class to set up a new Python project (package or backend).

    This class inherits from the Operation class and provides functionality
    to set up either a Python package or a backend project based on the
    provided parameters.

    Attributes
    ----------
        project_name (str): The name of the project to be created.
        is_backend (bool): Flag to determine if the project is a backend (True)
                           or a package (False).

    Methods
    -------
        execute: Executes the appropriate setup based on the project type.

    """

    def __init__(self, package_name: str, is_backend: bool = False):
        """Initialize the SetupNewPythonProject instance.

        Args:
        ----
            package_name (str): The name of the package to be created.
            is_backend (bool, optional): Flag to determine if the project is a
                                         backend. Defaults to False.

        """
        super().__init__()
        self.package_name = package_name
        self.is_backend = is_backend

    async def execute(self, *args: Any, **kwargs: Any):
        """Execute the appropriate setup based on project type.

        This method determines whether to set up a Python backend or a Python
        package based on the `is_backend` flag, and then executes the
        corresponding setup operation.

        Args:
        ----
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
        -------
            The result of the executed setup operation.

        Raises:
        ------
            Any exceptions raised by the underlying setup classes.

        """
        if self.is_backend:
            return await SetupPythonBackend(os.getcwd()).execute()
        else:
            return await SetupPythonPackage(self.package_name).execute()
        


# TODO: Add error handling for potential issues during project setup
# TODO: Implement logging to track the setup process
# IDEA: Consider adding a dry-run option to preview the setup steps without executing them
