"""
This module provides utilities for searching files and directories.
"""

import fnmatch
import os
from typing import List, Optional

from ...services.logging.custom_logger import CustomLogger

logger = CustomLogger(log_level="INFO")


def find_files_by_pattern(
    directory: str, pattern: str, recursive: bool = True, case_sensitive: bool = True
) -> List[str]:
    """
    Find files in a directory that match a pattern.

    Args:
        directory: The directory to search in
        pattern: The pattern to match against (glob pattern)
        recursive: Whether to search recursively in subdirectories
        case_sensitive: Whether the pattern matching should be case sensitive

    Returns:
        A list of file paths that match the pattern
    """
    matches = []
    if not case_sensitive:
        pattern = pattern.lower()

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if not case_sensitive:
                filename_to_match = filename.lower()
            else:
                filename_to_match = filename

            if fnmatch.fnmatch(filename_to_match, pattern):
                matches.append(os.path.join(root, filename))

        if not recursive:
            break

    return matches


def find_files_by_content(
    directory: str,
    content: str,
    file_pattern: Optional[str] = None,
    recursive: bool = True,
    case_sensitive: bool = True,
) -> List[str]:
    """
    Find files that contain specific content.

    Args:
        directory: The directory to search in
        content: The content to search for
        file_pattern: Optional pattern to filter files (glob pattern)
        recursive: Whether to search recursively in subdirectories
        case_sensitive: Whether the content matching should be case sensitive

    Returns:
        A list of file paths that contain the content
    """
    matches = []
    if not case_sensitive:
        content = content.lower()

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if file_pattern and not fnmatch.fnmatch(filename, file_pattern):
                continue

            try:
                with open(os.path.join(root, filename), "r", encoding="utf-8") as file:
                    file_content = file.read()
                    if not case_sensitive:
                        file_content = file_content.lower()

                    if content in file_content:
                        matches.append(os.path.join(root, filename))
            except (IOError, UnicodeDecodeError) as e:
                logger.info(f"Could not read file {filename}: {e}")

        if not recursive:
            break

    return matches
