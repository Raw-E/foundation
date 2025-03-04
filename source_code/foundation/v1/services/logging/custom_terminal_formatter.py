from datetime import datetime
import logging
import os
import shutil
from typing import Dict

from colorama import Back, Fore, Style


class CustomTerminalFormatter(logging.Formatter):
    TERMINAL_CONTROLS = {
        "CLEAR_LINE": "\033[K",
        "UNDERLINE_START": "\033[4m",
        "UNDERLINE_END": "\033[24m",
        "PURPLE_BACKGROUND": "\033[48;5;54m",
        "BRIGHT_CYAN": "\033[38;5;159m",
    }

    LOG_LEVEL_STYLES: Dict[str, tuple[str, str]] = {
        "TRACE": (f"{Style.DIM}{Fore.WHITE}", "🔬"),
        "INSPECT": (f"{Style.DIM}{Fore.GREEN}", "🛠️"),
        "SEARCH": (f"{Style.NORMAL}{Fore.BLUE}", "🔍"),
        "OBSERVE": (f"{Style.BRIGHT}{Fore.CYAN}", "👀"),
        "INFO": (f"{Style.NORMAL}{Fore.WHITE}", "ℹ️"),
        "CONCERN": (f"{Style.DIM}{Fore.YELLOW}", "🤔"),
        "SUSPECT": (f"{Style.BRIGHT}{Fore.RED}", "🐛"),
        "ERROR": (f"{Style.BRIGHT}{Back.LIGHTMAGENTA_EX}{Fore.WHITE}", "🚨"),
        "DANGER": (f"{Style.BRIGHT}{Back.LIGHTRED_EX}{Fore.WHITE}", "⛔️"),
        "SHOWSTOPPER": (f"{Style.DIM}{Back.BLACK}{Fore.RED}", "💀"),
    }

    METADATA_PREFIXES = {
        "LOCATION": "📍 Location:",
        "PACKAGE": "🔹 Package:",
        "FILE": "🔹 File:",
        "CALLED_FROM": "🔹 Called From:",
        "PATH": "🔹 Path:",
        "CALLED_BY": "↳ Called By:",
        "TIMESTAMP": "⏰ Time:",
    }

    MESSAGE_BODY_COLOR = f"{Style.NORMAL}{Fore.WHITE}"
    MESSAGE_HEADER_COLOR = f"{Style.BRIGHT}{Back.LIGHTYELLOW_EX}{Fore.BLACK}"
    BORDER_STYLE = f"{Style.BRIGHT}{Back.WHITE}{Fore.BLACK}"
    BORDER_CHARACTER = "═"
    METADATA_SECTION_SEPARATOR = "\nLOG CONTENT:\n"
    MESSAGE_BODY_HEADER = "======== LOG CONTENT ========"
    LOG_LEVEL_LABEL = "LOG ENTRY"

    @property
    def terminal_width(self) -> int:
        return shutil.get_terminal_size().columns

    def _format_path(self, path: str) -> str:
        abs_path = os.path.abspath(path.strip())
        return f"{self.TERMINAL_CONTROLS['PURPLE_BACKGROUND']}{self.TERMINAL_CONTROLS['UNDERLINE_START']}{abs_path}{self.TERMINAL_CONTROLS['UNDERLINE_END']}"

    def _format_metadata_section(
        self, record: logging.LogRecord, metadata_text: str, style: str, emoji: str
    ) -> str:
        current_time = datetime.fromtimestamp(record.created)
        timestamp = f"{current_time.strftime('%I:%M %p')} ({current_time.second}s {current_time.microsecond // 1000}ms {current_time.microsecond % 1000}μs)"
        path_marker = self.METADATA_PREFIXES["PATH"]

        location_lines = [
            f"{' ' * (len(line) - len(line.lstrip()))}{style}"
            + (
                f"{path_marker} {self._format_path(line.strip().split(':', 1)[1])}"
                if path_marker in line
                else line.strip()
            )
            + Style.RESET_ALL
            for line in metadata_text.split("\n")
            if line.strip()
        ]

        return "\n".join(
            [
                f"\n{style}{emoji}  {record.levelname} {self.LOG_LEVEL_LABEL}{Style.RESET_ALL}",
                f"    {style}{self.METADATA_PREFIXES['TIMESTAMP']} {timestamp}{Style.RESET_ALL}",
                *location_lines,
            ]
        )

    def format(self, record: logging.LogRecord) -> str:
        metadata, message = str(record.msg).split(self.METADATA_SECTION_SEPARATOR, 1)
        style, emoji = self.LOG_LEVEL_STYLES.get(record.levelname, self.LOG_LEVEL_STYLES["INFO"])
        border = f"{self.BORDER_STYLE}{self.BORDER_CHARACTER * self.terminal_width}{Style.RESET_ALL}{self.TERMINAL_CONTROLS['CLEAR_LINE']}"

        return "\n".join(
            [
                "",
                border,
                self._format_metadata_section(record, metadata, style, emoji),
                f"\n{self.MESSAGE_HEADER_COLOR}{self.MESSAGE_BODY_HEADER}{Style.RESET_ALL}",
                f"\n{self.MESSAGE_BODY_COLOR}{message.strip()}\n{Style.RESET_ALL}",
                border,
            ]
        )
