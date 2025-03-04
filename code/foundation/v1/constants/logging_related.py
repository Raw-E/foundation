import logging
from colorama import Fore, Style
from typing import Dict, Any

# Define constants for log levels
LOG_LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# List of loggers to ignore to reduce noise from third-party libraries
DEFAULT_LOGGERS_TO_IGNORE = [
    "asyncio", "asyncio.*", "boto3", "botocore", "chardet",
    "charset_normalizer", "concurrent", "httpx", "matplotlib",
    "multiprocessing", "paramiko", "PIL", "requests",
    "s3transfer", "urllib3"
]

# Default logging configuration with colorized output
DEFAULT_LOGGING_CONFIGURATION: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": (
                f"\n{'-' * 121}\n"
                f"{Fore.BLUE}From Custom Logger:\n"
                f"    -> Level: %(levelname)s\n"
                f"    -> Time Logged: %(asctime)s\n"
                f"    -> Logged From: %(name)s\n"
                f"        -> At Line Number: %(lineno)d{Style.RESET_ALL}\n\n"
                f"%(message)s\n"
                f"{'-' * 121}"
            ),
            "datefmt": "%I:%M:%S %p on %Y-%m-%d"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO"
        },
        **{logger: {"level": "WARNING"} for logger in DEFAULT_LOGGERS_TO_IGNORE}
    }
}