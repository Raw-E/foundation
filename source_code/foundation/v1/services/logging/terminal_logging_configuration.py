import logging
import logging.config
from typing import Any, Dict

from .custom_terminal_formatter import CustomTerminalFormatter

DEFAULT_LOGGERS_TO_IGNORE: list[str] = ["fsevents", "watchfiles"]

DEFAULT_LOGGING_CONFIGURATION: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep existing loggers active - allows third-party loggers to function and custom configuration to coexist
    "formatters": {
        "custom_terminal_formatter": {
            "()": "logging.TerminalFormatter",
        },
        "basic_formatter": {"format": "\n" + "-" * 120 + "\n%(levelname)s - %(name)s - %(message)s\n" + "-" * 120},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "basic_formatter",  # Use basic formatter for root logger
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        **{
            logger: {
                "propagate": False  # Prevent messages from reaching the root logger
            }
            for logger in DEFAULT_LOGGERS_TO_IGNORE
        },
    },
}


def setup_logging() -> None:
    logging.TerminalFormatter = CustomTerminalFormatter  # type: ignore
    logging.config.dictConfig(DEFAULT_LOGGING_CONFIGURATION)
