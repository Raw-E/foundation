"""
This module provides general filesystem utilities.
"""

import os
from pathlib import Path
import shutil
from typing import List, Optional, Union

import aiofiles

from ...services.logging.custom_logger import CustomLogger

logger = CustomLogger()


def ensure_directory_exists(directory_path: Union[str, Path]) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: The path to the directory
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def remove_directory(directory_path: Union[str, Path], ignore_errors: bool = False) -> None:
    """
    Remove a directory and all its contents.

    Args:
        directory_path: The path to the directory to remove
        ignore_errors: Whether to ignore errors during removal
    """
    try:
        shutil.rmtree(directory_path, ignore_errors=ignore_errors)
    except Exception as e:
        if not ignore_errors:
            logger.error(f"Error removing directory {directory_path}: {e}")
            raise


def copy_file(
    source_path: Union[str, Path],
    destination_path: Union[str, Path],
    overwrite: bool = False,
) -> None:
    """
    Copy a file from source to destination.

    Args:
        source_path: The path to the source file
        destination_path: The path to the destination file
        overwrite: Whether to overwrite the destination file if it exists

    Raises:
        FileNotFoundError: If the source file does not exist
        FileExistsError: If the destination file exists and overwrite is False
        IOError: If there is an error copying the file
    """
    try:
        source_path = Path(source_path)
        destination_path = Path(destination_path)

        if not source_path.exists():
            raise FileNotFoundError(f"Source file does not exist: {source_path}")

        if destination_path.exists() and not overwrite:
            raise FileExistsError(f"Destination file already exists: {destination_path}")

        # Ensure the destination directory exists
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_path, destination_path)
    except Exception as e:
        logger.error(f"Error copying file from {source_path} to {destination_path}: {e}")
        raise


def copy_directory(
    source_path: Union[str, Path],
    destination_path: Union[str, Path],
    ignore_patterns: Optional[List[str]] = None,
) -> None:
    """
    Copy a directory and its contents.

    Args:
        source_path: The path to the source directory
        destination_path: The path to the destination directory
        ignore_patterns: List of patterns to ignore during copying
    """
    try:
        if ignore_patterns:
            shutil.copytree(
                source_path,
                destination_path,
                ignore=shutil.ignore_patterns(*ignore_patterns),
                dirs_exist_ok=True,
            )
        else:
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    except Exception as e:
        logger.error(f"Error copying directory from {source_path} to {destination_path}: {e}")
        raise


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path: The path to the file

    Returns:
        The size of the file in bytes
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        raise


def get_directory_size(directory_path: Union[str, Path]) -> int:
    """
    Get the total size of a directory and its contents in bytes.

    Args:
        directory_path: The path to the directory

    Returns:
        The total size in bytes
    """
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size
    except Exception as e:
        logger.error(f"Error calculating directory size for {directory_path}: {e}")
        raise


async def read_file_contents_asynchronously(file_path: Union[str, Path]) -> str:
    """
    Read the contents of a file asynchronously.

    Args:
        file_path: The path to the file to read

    Returns:
        The contents of the file as a string

    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there is an error reading the file
    """
    try:
        async with aiofiles.open(file_path, mode="r") as file:
            return await file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise


def copy_file_or_directory(
    source_path: Union[str, Path],
    destination_path: Union[str, Path],
    overwrite: bool = False,
    ignore_patterns: Optional[List[str]] = None,
) -> None:
    """
    Copy a file or directory from source to destination.

    Args:
        source_path: The path to the source file or directory
        destination_path: The path to the destination file or directory
        overwrite: Whether to overwrite the destination if it exists
        ignore_patterns: List of patterns to ignore during copying (only applies to directories)

    Raises:
        FileNotFoundError: If the source does not exist
        FileExistsError: If the destination exists and overwrite is False
        IOError: If there is an error copying
    """
    source_path = Path(source_path)

    if not source_path.exists():
        raise FileNotFoundError(f"Source does not exist: {source_path}")

    if source_path.is_file():
        copy_file(source_path, destination_path, overwrite=overwrite)
    else:
        copy_directory(source_path, destination_path, ignore_patterns=ignore_patterns)


def create_directory_safely(directory_path: Union[str, Path], overwrite: bool = False) -> Path:
    """
    Create a directory safely, with options to handle existing directories.

    Args:
        directory_path: The path to the directory to create
        overwrite: Whether to remove the directory if it already exists

    Returns:
        Path: The path to the created directory

    Raises:
        FileExistsError: If the directory exists and overwrite is False
        IOError: If there is an error creating the directory
    """
    directory_path = Path(directory_path)

    if directory_path.exists():
        if not overwrite:
            raise FileExistsError(f"Directory already exists: {directory_path}")
        remove_directory(directory_path)

    ensure_directory_exists(directory_path)
    return directory_path


def rename_subdirectory(
    parent_directory: Union[str, Path],
    old_name: str,
    new_name: str,
    overwrite: bool = True,
) -> None:
    """
    Rename a subdirectory within a parent directory.

    Args:
        parent_directory: The path to the parent directory
        old_name: The current name of the subdirectory
        new_name: The new name for the subdirectory
        overwrite: Whether to overwrite the destination if it exists

    Raises:
        FileNotFoundError: If the source directory does not exist
        FileExistsError: If the destination directory exists and overwrite is False
        IOError: If there is an error during renaming
    """
    parent_directory = Path(parent_directory)
    old_path = parent_directory / old_name
    new_path = parent_directory / new_name

    if not old_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {old_path}")

    if new_path.exists():
        if not overwrite:
            raise FileExistsError(f"Destination directory already exists: {new_path}")
        try:
            remove_directory(new_path)
        except Exception as error:
            logger.error(f"Error removing existing directory {new_path}: {error}")
            raise

    try:
        # First try atomic rename
        old_path.rename(new_path)
    except OSError:
        # If atomic rename fails, try copy and remove
        try:
            shutil.copytree(old_path, new_path)
            remove_directory(old_path)
        except Exception as error:
            # If copy fails, clean up any partial new directory
            if new_path.exists():
                try:
                    remove_directory(new_path)
                except Exception:
                    pass  # Best effort cleanup
            logger.error(f"Error during directory rename from {old_path} to {new_path}: {error}")
            raise


async def update_text_in_files(
    file_paths: List[Union[str, Path]],
    old_text: str,
    new_text: str,
    file_extensions: Optional[tuple[str, ...]] = None,
) -> None:
    """
    Update text content in multiple files asynchronously.

    Args:
        file_paths: List of paths to files or directories that need to be updated
        old_text: The text to be replaced
        new_text: The replacement text
        file_extensions: Optional tuple of file extensions to process (e.g., ('.py', '.txt'))

    Raises:
        FileNotFoundError: If any of the files do not exist
        IOError: If there is an error reading or writing any file
    """
    # Directories to skip
    skip_dirs = {".git", ".ruff_cache", ".pytest_cache", "__pycache__", ".venv"}

    for path in file_paths:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")

        if path.is_file():
            if file_extensions and not str(path).lower().endswith(file_extensions):
                continue
            try:
                # Try to read the first few bytes to check if it's a text file
                with open(path, "rb") as f:
                    is_binary = b"\0" in f.read(1024)
                if is_binary:
                    continue

                # Read and update the file content
                content = await read_file_contents_asynchronously(path)
                updated_content = content.replace(old_text, new_text)

                # Write back to the file
                async with aiofiles.open(path, mode="w") as file:
                    await file.write(updated_content)
            except UnicodeDecodeError:
                # Skip files that can't be decoded as text
                continue
            except Exception as e:
                logger.error(f"Error updating text in file {path}: {e}")
                raise
        else:  # Directory
            # Process all files in the directory recursively
            for file_path in path.rglob("*"):
                # Skip specified directories
                if any(skip_dir in str(file_path.parent) for skip_dir in skip_dirs):
                    continue

                if file_path.is_file():
                    if file_extensions and not str(file_path).lower().endswith(file_extensions):
                        continue
                    try:
                        # Try to read the first few bytes to check if it's a text file
                        with open(file_path, "rb") as f:
                            is_binary = b"\0" in f.read(1024)
                        if is_binary:
                            continue

                        # Read and update the file content
                        content = await read_file_contents_asynchronously(file_path)
                        updated_content = content.replace(old_text, new_text)

                        # Write back to the file
                        async with aiofiles.open(file_path, mode="w") as file:
                            await file.write(updated_content)
                    except UnicodeDecodeError:
                        # Skip files that can't be decoded as text
                        continue
                    except Exception as e:
                        logger.error(f"Error updating text in file {file_path}: {e}")
                        raise
