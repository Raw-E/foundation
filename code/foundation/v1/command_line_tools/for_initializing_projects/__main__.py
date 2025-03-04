"""Module: __main__.py

This module serves as the entry point for the automatic project setup tool.
It handles command-line argument parsing and initiates the project setup process.

Functions:
    - parse_arguments(): Parse command-line arguments
    - main(project_name: str, is_backend: bool): Initiates the project setup
    - cli(): Entry point for the command-line interface

Usage:
    Run this module directly to use the automatic project setup tool:
    python -m dev_pytopia.v1.command_line_tools.automatic_project_setuper <project_name> [--backend]

Dependencies:
    - argparse
    - asyncio
    - sys
    - .setup_python_project.SetupPythonProject

For detailed documentation, see the individual function docstrings.
"""

# Standard library imports
import asyncio
import sys

# Local application imports
from .operations.setup_python_project import SetupPythonProject
from .utilities import parse_arguments

async def main(package_name: str, is_backend: bool) -> None:
    """Initiate the project setup.

    Args:
        project_name (str | None): The name of the new package or folder for the backend. 
                                   Can be None for backend projects.
        is_backend (bool): Flag indicating whether to create a backend project.

    Raises:
        Exception: If an error occurs during the setup process.
    """
    # Create a SetupPythonProject instance and execute the setup process
    await SetupPythonProject(package_name, is_backend=is_backend)

def cli() -> None:
    """Entry point for the command-line interface.

    This function serves as the main entry point for the CLI. It calls the
    argument parsing function, calls the main() function, and manages error handling.

    If an exception occurs, it prints the error message to stderr and exits
    with a non-zero status code.
    """
    args = parse_arguments()

    try:
        asyncio.run(main(args.package_name, args.backend))
    except Exception as e:
        print(f"An error occurred during project setup: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli()

# TODO: Consider adding support for configuration files to customize the setup process
# IDEA: Implement a dry-run mode to preview the setup process without making changes