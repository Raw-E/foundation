from enum import IntEnum
import inspect
import logging
import logging.config
import os
from typing import Any, Dict

from .custom_terminal_formatter import CustomTerminalFormatter
from .operations.get_location_of_log_call import GetLocationOfLogCall


class LogLevel(IntEnum):
    TRACE = 0
    INSPECT = 1
    SEARCH = 2
    OBSERVE = 3
    INFO = 4
    CONCERN = 5
    SUSPECT = 6
    ERROR = 7
    DANGER = 8
    SHOWSTOPPER = 9


class CustomLogger(logging.Logger):
    LOG_LEVEL_MAP: Dict[str, int] = {level.name: level.value for level in LogLevel}
    [logging.addLevelName(level_value, level_name) for level_name, level_value in LOG_LEVEL_MAP.items()]

    trace: Any
    inspect: Any
    search: Any
    observe: Any
    info: Any
    concern: Any
    suspect: Any
    error: Any
    danger: Any
    showstopper: Any

    def __init__(self, log_level: str = "INFO") -> None:
        self._validate_log_level(log_level)
        super().__init__(self._determine_logger_name())
        self._setup_handler_and_formatter(log_level)
        self._add_log_methods()

    def _validate_log_level(self, log_level: str) -> None:
        if log_level.upper() not in self.LOG_LEVEL_MAP:
            raise ValueError(
                f"Invalid log level: {log_level}. Must be one of {', '.join(self.LOG_LEVEL_MAP.keys())}"
            )

    def _determine_logger_name(self) -> str:
        frame = inspect.currentframe()
        path = os.path.relpath(frame.f_back.f_code.co_filename)  # type: ignore
        return path[:-3] if path.endswith(".py") else path

    def _setup_handler_and_formatter(self, log_level: str) -> None:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomTerminalFormatter())
        self.addHandler(handler)

        level = self.LOG_LEVEL_MAP[log_level.upper()]
        self.setLevel(level)
        handler.setLevel(level)

    def _add_log_methods(self) -> None:
        for level in LogLevel:
            setattr(
                self,
                level.name.lower(),
                lambda msg, *args, level=level.value, **kwargs: self._log_with_location(
                    level, msg, *args, **kwargs
                ),
            )

    def _log_with_location(
        self,
        level: int,
        msg: str,
        stack_level: int = 1,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        caller_frame = inspect.currentframe()
        caller_frame = caller_frame.f_back if caller_frame else None

        location_text = GetLocationOfLogCall(caller_frame=caller_frame, stack_level=stack_level)()
        kwargs.update({"extra": {"location_info": True}})
        self.log(level, f"{location_text}\n\nLOG CONTENT:\n\n{msg}", *args, **kwargs)
