"""Module: setup_python_package.py

This module provides functionality for setting up a new Python package project.

It contains a class that handles the creation of a new package directory,
copying template files, and updating package references.

Classes:
    - SetupPythonPackage: Handles the setup process for a new Python package.

Usage:
    from setup_python_package import SetupPythonPackage

    # Create a new package
    setup = SetupPythonPackage("my_new_package")
    new_project_dir = await setup.execute()

Dependencies:
    - os
    - typing
    - universal_utility_functions.filesystem_related.general_filesystem_utilities
    - operation_framework.operation

For detailed documentation, see the individual class and method docstrings.
"""

# Standard library imports
import os
from typing import Any

from ....operation_framework.operation import Operation

# Local application imports
from ....universal_utility_functions.filesystem_related.general_filesystem_utilities import (
    copy_file_or_directory,
    create_directory_safely,
    rename_subdirectory,
    update_text_in_files,
)

# Constants
PYTHON_PACKAGE_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "python_package_template")
PYTHON_PACKAGES_DIR = os.path.expanduser("~/Desktop/Useful Python Things/My Packages")


class SetupPythonPackage(Operation):
    """Class to set up a new Python package project.

    This class handles the process of creating a new Python package,
    including directory creation, template copying, and reference updating.

    Attributes
    ----------
        project_name (str): The name of the new Python package.

    Methods
    -------
        execute: Main method to execute the package setup process.
        create_package_directory: Creates the new package directory.
        update_package_references: Updates package name references in project files.

    """

    def __init__(self, package_name: str):
        """Initialize the SetupPythonPackage instance.

        Args:
        ----
            project_name (str): The name of the new Python package.

        """
        super().__init__()
        self.package_name = package_name

    async def execute(self, *args: Any, **kwargs: Any) -> str:
        """Execute the package project setup process.

        This method orchestrates the entire setup process, including:
        1. Creating the package directory
        2. Copying template files
        3. Renaming the source directory
        4. Updating package references

        Returns
        -------
            str: The path to the newly created project directory.

        """
        # Create the root directory name with capitalized words
        root_dir_name = "-".join(word.capitalize() for word in self.package_name.split("_"))

        # Create the new project directory
        new_project_dir = self.create_package_directory(PYTHON_PACKAGES_DIR, root_dir_name)

        if new_project_dir:
            # Copy template files to the new project directory
            copy_file_or_directory(PYTHON_PACKAGE_TEMPLATE_DIR, new_project_dir)

            # Rename the source directory to match the new package name
            rename_subdirectory(new_project_dir, "src/package_name", f"src/{self.package_name}")

            # Update package references in all project files
            self.update_package_references(new_project_dir, self.package_name)

        return new_project_dir

    @staticmethod
    def create_package_directory(python_package_dir: str, root_dir_name: str) -> str:
        """Create the new package directory.

        Args:
        ----
            python_package_dir (str): The parent directory for Python packages.
            root_dir_name (str): The name of the root directory for the new package.

        Returns:
        -------
            str: The path to the newly created package directory.

        """
        new_package_dir = os.path.join(python_package_dir, root_dir_name)
        return create_directory_safely(new_package_dir)

    @staticmethod
    def update_package_references(new_package_dir: str, new_package_name: str):
        """Update package name references in all project files.

        This method replaces placeholder text with the actual package name
        in various formats (e.g., with underscores, with hyphens, capitalized).

        Args:
        ----
            new_package_dir (str): The directory of the new package.
            new_package_name (str): The name of the new package.

        """
        replacements = {
            "<package_name>": new_package_name,
            "<package_name>".replace("_", "-"): new_package_name.replace("_", "-"),
            "<Package Name>": " ".join(word.capitalize() for word in new_package_name.split("_")),
        }
        update_text_in_files(new_package_dir, replacements, file_extensions=(".py", ".md", ".txt", ".toml"))


# TODO: Add error handling for file operations
# TODO: Implement logging for better debugging and tracking of the setup process
# IDEA: Add a configuration file option for customizing the setup process
