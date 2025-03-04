# THIS CODE HAS BEEN ORGANIZED

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║ Documentation for file_name.py
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Standard library imports
from typing import Protocol, Set

# Third-party imports
from watchfiles import Change

# Local development package imports
from ..logging.custom_logger import CustomLogger

# Current project imports
from .file_system_observer import FileSystemObserver, FileSystemObserverConfiguration

# Configuration
logger = CustomLogger(log_level="INFO")


# Classes
class FileSystemChangeResponder(Protocol):
    def _should_process_change(self, event_path: str) -> bool: ...
    def _handle_directory_change(self, changes: Set[tuple[Change, str]]) -> None: ...


class FileSystemChangeProcessor:
    def __init__(
        self,
        observer_configuration: FileSystemObserverConfiguration,
        file_system_change_responder: FileSystemChangeResponder,
    ) -> None:
        self.file_system_change_responder = file_system_change_responder
        self.observer = FileSystemObserver(observer_configuration)

    async def process_changes(self) -> None:
        async for changes in self.observer.observe():
            changes_to_process = {
                (change, path)
                for change, path in changes
                if self.file_system_change_responder._should_process_change(path)
                and path != self.observer.config.processing_lock_file
                and not self.observer.is_lock_file_present()
            }
            if changes_to_process:
                self.file_system_change_responder._handle_directory_change(changes_to_process)

    def stop_observing(self) -> None:
        self.observer.stop()
