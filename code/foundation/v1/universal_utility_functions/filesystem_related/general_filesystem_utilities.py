"""
General Filesystem Utilities

This module provides a collection of utility functions for various filesystem operations,
including file and directory handling, content manipulation, path validation, and call stack inspection.

Functions:
    copy_file_or_directory: Copy a file or directory to a specified destination.
    traverse_directory: Recursively traverse a directory, yielding file or directory paths.
    update_text_in_files: Update text in files across a directory structure.
    create_directory_safely: Create a directory if it doesn't exist or use it if empty.
    rename_subdirectory: Rename a subdirectory within a given directory.
    validate_path: Check if a given path exists.
    update_file_content: Update file content based on a specified condition.
    get_caller_module_name: Get the full module path of the calling function.
    read_file_contents: Safely read and return the contents of a specified file.

Usage:
    from dev_pytopia.v1.universal_utility_functions.filesystem_related.general_filesystem_utilities import *

    # Copy a file or directory
    copy_file_or_directory('/source/path', '/destination/path')

    # Traverse a directory
    for path in traverse_directory("/root/dir", file_extension=".py", include_dirs=True):
        print(path)

    # Update text in files
    update_text_in_files("/target/dir", {"old_text": "new_text"}, ('.py', '.txt'))

    # Create a directory safely
    new_dir = create_directory_safely("/path/to/new/directory")

    # Rename a subdirectory
    rename_subdirectory("/parent/dir", "old_name", "new_name")

    # Validate a path
    if validate_path("/path/to/check"):
        print("Path exists")

    # Update file content
    update_file_content("/path/to/file.txt", "New content", 
                        condition=lambda content: len(content) < 100)

    # Get the caller's module name
    caller_module = get_caller_module_name()
    print(f"This function was called from: {caller_module}")

    # Get the caller's caller module name
    caller_caller_module = get_caller_module_name(levels_up=2)
    print(f"The function that called this function was called from: {caller_caller_module}")

    # Read file contents
    content = read_file_contents("/path/to/file.txt")
    print(content)

Dependencies:
    os, shutil, typing, inspect

For detailed information, refer to individual function docstrings.
"""

# Standard library imports
import os
import shutil
import inspect
from typing import Dict, Iterator, Optional, Union
from pathlib import Path 

# Third-party imports
# None for this module

# Local application imports
from ..logging_related import get_custom_logger

logger = get_custom_logger()

def copy_file_or_directory(source: str, destination: str) -> None:
    """Copy a file or directory to the specified destination.

    Args:
    ----
        source (str): Path to the source file or directory.
        destination (str): Path to the destination.

    Raises:
    ------
        FileNotFoundError: If the source path does not exist.

    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source path '{source}' does not exist.")

    if os.path.isdir(source):
        # If source is a directory, use copytree
        # NOTE: The behavior of copytree with dirs_exist_ok=True is as follows:
        # 1. If destination doesn't exist:
        #    - A new directory is created at the destination path
        #    - The entire contents of the source directory are copied into it
        # 2. If destination already exists:
        #    - The contents of the source are copied directly into the existing destination directory
        #    - No new subdirectory named after the source is created
        #    - Existing files with the same names are overwritten
        #    - New files and directories are added
        #    - Existing files and directories in the destination that don't exist in the source remain unchanged
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        # If source is a file, use copy2
        # This will copy the file to the destination, creating parent directories if needed
        # If a file with the same name exists at the destination, it will be overwritten
        shutil.copy2(source, destination)


def traverse_directory(
    root_directory: str,
    file_extension_filter: Optional[str | list[str]] = None,
    include_dirs: bool = False,
) -> Iterator[str]:
    """Yield file and directory paths recursively from a root directory.
    
    Args:
        root_directory: Starting directory for traversal
        file_extension_filter: Optional filter for file types (e.g., ".py" or [".py", ".pyw"])
                             Can be a single extension or list of extensions
        include_dirs: If True, include directory paths in output
    
    Yields:
        Full paths to matching files and directories
    
    Example:
        # Get all Python files
        python_files = list(traverse_directory("./src", COMMON_FILE_EXTENSIONS['python']))
        
        # Get all image files
        image_files = list(traverse_directory("./assets", COMMON_FILE_EXTENSIONS['images']))
    """
    # Convert single extension to list for consistent handling
    if isinstance(file_extension_filter, str):
        file_extension_filter = [file_extension_filter]

    for root, dirs, files in os.walk(root_directory):
        # Yield directories first if requested
        if include_dirs:
            yield from map(lambda d: os.path.join(root, d), dirs)
        
        # Yield files matching extension filter (or all if no filter)
        yield from (
            os.path.join(root, f) 
            for f in files 
            if not file_extension_filter or any(f.endswith(ext) for ext in file_extension_filter)
        )

def update_text_in_files(directory, replacements, file_extensions=None):
    """Update text in files across a directory structure.

    :param directory: The root directory to start the search from.
    :param replacements: A dictionary of {old_text: new_text} pairs.
    :param file_extensions: A tuple of file extensions to process (e.g., ('.py', '.txt')).
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file_extensions is None or file.endswith(file_extensions):
                file_path = os.path.join(root, file)
                with open(file_path) as f:
                    content = f.read()

                for old_text, new_text in replacements.items():
                    content = content.replace(old_text, new_text)

                with open(file_path, "w") as f:
                    f.write(content)


def create_directory_safely(directory):
    """Create a directory if it doesn't exist, or use it if it's empty.

    :param directory: The directory path to create.
    :return: The path of the created or existing directory.
    :raises FileExistsError: If the directory exists and is not empty.
    """
    if os.path.exists(directory):
        if os.listdir(directory):
            raise FileExistsError(f"Directory '{directory}' already exists and is not empty.")
    else:
        os.makedirs(directory)
    return directory


def rename_subdirectory(parent_dir, old_name, new_name):
    """Rename a subdirectory within a given directory.

    :param parent_dir: The parent directory containing the subdirectory to be renamed.
    :param old_name: The current name of the subdirectory.
    :param new_name: The new name for the subdirectory.
    """
    old_path = os.path.join(parent_dir, old_name)
    new_path = os.path.join(parent_dir, new_name)
    os.rename(old_path, new_path)

def update_file_content(file_path: str, new_content: str, condition: Optional[callable] = None) -> None:
    file_handle = None
    try:
        file_handle = open(file_path, "r+")
        current_content = file_handle.read()
        should_update = condition is None or condition(current_content)

        if current_content == new_content:
            logger.info(f"No update needed - content already matches in {file_path}")
            return
            
        if should_update:
            logger.info(f"Updating file: {file_path}")
            file_handle.seek(0)
            file_handle.write(new_content)
            file_handle.truncate()
            file_handle.flush()
            os.fsync(file_handle.fileno())
            
    except IOError as e:
        raise IOError(f"Error updating file {file_path}: {str(e)}")
    finally:
        if file_handle:
            file_handle.close()

def get_caller_module_name(levels_up: int = 1) -> str:
    """
    Get the full module path of the calling function.

    This function inspects the call stack to determine the module name of the function
    that called the current function. It allows flexibility in how far up the call stack
    to look, which can be useful in various scenarios.

    Args:
    ----
        levels_up (int): Number of levels up in the call stack to look. 
                         Default is 1 (immediate caller).
                         Use 2 for the caller's caller, 3 for its caller, and so on.

    Returns:
    -------
        str: The full module path of the caller.

    Example:
    -------
        # In module 'my_package.my_module':
        def my_function():
            print(get_caller_module_name())  # Prints the module calling my_function
            print(get_caller_module_name(2))  # Prints the module calling the function that called my_function

    Note:
    ----
        - If the caller is in the main script (not in a module), this function
          will return the script's filename without the '.py' extension.
        - Be cautious when using levels_up > 1, as it may raise an IndexError
          if there aren't enough stack frames.

    Raises:
    ------
        IndexError: If levels_up is greater than the number of available stack frames.
    """
    caller_frame = inspect.stack()[levels_up]
    caller_module = inspect.getmodule(caller_frame[0])
    if caller_module:
        return caller_module.__name__
    else:
        return os.path.splitext(caller_frame.filename)[0].replace(os.path.sep, '.')

def read_file_contents(file_path: Path, encoding: str = "utf-8") -> str:
    """
    Safely read and return the contents of a specified file.

    This function handles various exceptions that may occur during file reading,
    providing more informative error messages.

    Args:
        file_path (Path): The path to the file to be read.
        encoding (str, optional): The encoding to use when reading the file. Defaults to "utf-8".

    Returns:
        str: The contents of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PermissionError: If the program lacks necessary permissions to read the file.
        IOError: For other I/O related errors, including encoding issues.
    """
    try:
        with file_path.open("r", encoding=encoding) as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        # Provide more context in the error message
        raise type(e)(f"{e.strerror}: '{file_path}'") from None
    except IOError as e:
        # Catch potential encoding errors and other I/O issues
        raise IOError(f"Error reading file '{file_path}': {e}") from None
    
def write_to_file(file_path: str, content: str, encoding: str = "utf-8") -> None:
    """
    Write content to a specified file, replacing any existing content.

    This function writes the given content to the specified file, overwriting
    any existing content. If the file does not exist, it creates a new file.

    Args:
        file_path (str): The path to the file to be written.
        content (str): The content to write to the file.
        encoding (str, optional): The encoding to use when writing to the file. Defaults to "utf-8".

    Raises:
        IOError: If there's an error writing to the file.
    """
    try:
        with open(file_path, "w", encoding=encoding) as file:
            file.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file '{file_path}': {e}") from None
    
def copy_directory(
    source_path: Path, 
    destination_path: Path, 
    overwrite: bool = False,
    base_filename: Optional[str] = None,
) -> None:
    """Copy all files from source directory to destination, preserving directory structure.
    
    This function performs a recursive directory copy operation, maintaining the original
    directory hierarchy while allowing for filename customization. It's particularly useful
    for template operations where you need to:
    1. Copy an entire directory structure (like a template)
    2. Optionally prefix all filenames with a base name
    3. Preserve the nested folder structure
    4. Handle file conflicts through the overwrite parameter
    
    Example:
        If copying a template directory with structure:
            template/
                ├── file1.txt
                └── subdir/
                    └── file2.txt
        
        With base_filename="MyProject":
            -> Creates:
                destination/
                    ├── MyProjectfile1.txt
                    └── subdir/
                        └── MyProjectfile2.txt
    
    Args:
        source_path: Source directory to copy from
        destination_path: Destination directory to copy to
        overwrite: Whether to overwrite existing files
        base_filename: Optional prefix for destination filenames
    """
    # Validate source directory exists
    if not source_path.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_path}")
    
    # Create destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    
    # Recursively process all files and directories
    for item in source_path.rglob("*"):
        # Calculate relative path to maintain directory structure
        relative_path = item.relative_to(source_path)
        
        if item.is_file():
            # Construct new filename with optional prefix
            new_filename = f"{base_filename}{relative_path.name}" if base_filename else relative_path.name
            # Calculate destination path preserving directory structure
            dest_file = destination_path / relative_path.parent / new_filename
            
            # Create parent directories if they don't exist
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle file copying based on overwrite flag
            if not dest_file.exists() or overwrite:
                logger.info(f"Copying file: {item} -> {dest_file}")
                shutil.copy2(item, dest_file)
            else:
                logger.warning(
                    f"Skipping existing file {dest_file}. "
                    "Set overwrite=True to replace existing files."
                )
        
        elif item.is_dir():
            # Create corresponding directory in destination
            new_dir = destination_path / relative_path
            new_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {new_dir}")

    logger.info(f"Directory copy completed: {source_path} -> {destination_path}")

def copy_file(
    source_path: Path,
    destination_path: Path,
    *, 
    overwrite: bool = False
) -> None:
    """Copy a single file from source to destination.
    
    Args:
        source_path: Source file to copy
        destination_path: Destination path for the copy
        overwrite: If False (default), raises FileExistsError when destination exists
                  If True, replaces any existing file at the destination
    
    Raises:
        FileExistsError: If destination exists and overwrite=False
        FileNotFoundError: If source file doesn't exist
    """
    # Check source first to fail fast if it doesn't exist
    if not source_path.is_file():
        raise FileNotFoundError(f"Source file does not exist: {source_path}")
        
    # Only check destination if overwrite=False
    if not overwrite and destination_path.exists():
        raise FileExistsError(
            f"Destination file already exists: {destination_path}. "
            "Set overwrite=True to replace existing files."
        )
    
    # Direct copy without additional checks since we've validated everything
    shutil.copy2(source_path, destination_path)

# TODO: Consider adding more filesystem-related utility functions
# IDEA: Implement a function to calculate directory size recursively


def is_file_empty(file_path: Union[Path, str]) -> bool:
    """
    Check if a file is empty.

    Args:
        file_path (Union[Path, str]): Path to the file to check

    Returns:
        bool: True if the file is empty, False otherwise

    Raises:
        FileNotFoundError: If the file doesn't exist (raised by Path operations)
        PermissionError: If the program lacks permission to access the file (raised by stat())
        IsADirectoryError: If the path points to a directory
    """
    path = Path(file_path) if isinstance(file_path, str) else file_path
    
    # Will raise FileNotFoundError if path doesn't exist
    # Will return False for directories, leading to IsADirectoryError below
    if not path.is_file():
        raise IsADirectoryError(f"Path {path} is not a regular file")
        
    # Will raise PermissionError if we lack read permissions
    return path.stat().st_size == 0

# async def fill_template_variables(file_path: Path, variables: Dict[str, str]) -> None:
#     """
#     Fills template variables in the given file.
    
#     Args:
#         file_path (Path): Path to the file to update.
#         variables (Dict[str, str]): Dictionary of template variables and their replacements.
        
#     IDEA: Make this function support synchronous operation as well for flexibility.
#     """
#     if file_path.exists():
#         content: str = file_path.read_text()
#         updated_content: str = content
#         for placeholder, replacement in variables.items():
#             updated_content = updated_content.replace(placeholder, replacement)
            
#         if content != updated_content:
#             file_path.write_text(updated_content)

async def fill_template_variables(file_path: Path, variables: Dict[str, str]) -> None:
    """
    Fills template variables in the given file.
    
    Args:
        file_path (Path): Path to the file to update.
        variables (Dict[str, str]): Dictionary of template variables and their replacements.
        
    IDEA: Make this function support synchronous operation as well for flexibility.
    """
    if file_path.exists():
        content: str = file_path.read_text()
        updated_content: str = content
        
        logger.debug(f"Processing template variables in {file_path}")
        logger.debug(f"Available variables: {variables}")
        
        for placeholder, replacement in variables.items():
            if placeholder in content:
                logger.info(f"Found variable '{placeholder}' in {file_path}")
                updated_content = updated_content.replace(placeholder, replacement)
                logger.debug(f"Replaced '{placeholder}' with '{replacement}'")
            else:
                logger.debug(f"Variable '{placeholder}' not found in {file_path}")
            
        if content != updated_content:
            logger.info(f"Updating content in {file_path}")
            file_path.write_text(updated_content)
        else:
            logger.debug(f"No changes needed in {file_path}")