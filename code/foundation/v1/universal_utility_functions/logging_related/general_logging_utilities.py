"""
This module provides a logging utility to configure and obtain custom loggers.

Features:
- Default logging configuration with colorized console output.
- Ability to ignore specific third-party loggers to reduce noise.
- Function to set up logging with a specified or default configuration.
- Function to obtain a custom logger with automatic naming based on the caller's module and file.
"""

# Standard library imports
import inspect
import logging
import logging.config
from typing import Optional, Type

from ...constants.logging_related import DEFAULT_LOGGING_CONFIGURATION, LOG_LEVEL_MAP

def get_custom_logger(name: Optional[str] = None, log_level: Optional[str] = 'INFO') -> logging.Logger:
    """
    Obtain a logger with automatic naming and specified log level.
    """
    if log_level.upper() not in LOG_LEVEL_MAP:
        raise ValueError(f"Invalid log level: {log_level}. Must be one of {', '.join(LOG_LEVEL_MAP.keys())}")
    
    logger: logging.Logger = logging.getLogger(name or generate_logger_name())
    logger.setLevel(LOG_LEVEL_MAP[log_level.upper()])
    logging.config.dictConfig(DEFAULT_LOGGING_CONFIGURATION)
    return logger

def generate_logger_name() -> str:
    """
    Generate a logger name based on the caller's module and file name.
    Returns "Unknown Caller" if the module name or file name cannot be identified.

    Returns:
        str: Generated logger name.
    """
    # Retrieve the current frame and go up two levels to get the caller's frame
    current_frame: Optional[inspect.FrameType] = inspect.currentframe()
    caller_frame: Optional[inspect.FrameType] = current_frame.f_back.f_back if current_frame and current_frame.f_back else None

    if caller_frame:
        module: Optional[Type[inspect.ModuleType]] = inspect.getmodule(caller_frame)
        file_name: Optional[str] = inspect.getfile(caller_frame) if inspect.getfile(caller_frame) else None

        module_name: str = module.__name__ if module and hasattr(module, '__name__') else "Unknown Module"
        file_part: str = f" ({file_name})" if file_name else " (Unknown File)"

        return f"{module_name}{file_part}"
    
    return "Unknown Caller"