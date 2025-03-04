# THIS CODE HAS BEEN ORGANIZED

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║ Documentation for file_name.py
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Standard library imports
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator, List, Optional, Sequence, Set, Union

# Third-party imports
from watchfiles import Change, awatch

# Local development package imports
from ..logging.custom_logger import CustomLogger

logger = CustomLogger(log_level="INFO")


@dataclass
class FileSystemObserverConfiguration:
    directories_to_observe: List[Path]
    include_patterns: List[str]
    exclude_patterns: List[str]
    processing_lock_file: Optional[str] = None

    def __init__(
        self,
        directories_to_observe: Union[str, Path, Sequence[Union[str, Path]]],
        include_patterns: List[str],
        exclude_patterns: List[str],
        processing_lock_file: Optional[str] = None,
    ) -> None:
        if isinstance(directories_to_observe, (str, Path)):
            directories_to_observe = [directories_to_observe]

        self.directories_to_observe = [Path(str(directory)) for directory in directories_to_observe]
        self.include_patterns = [pattern.strip() for pattern in include_patterns]
        self.exclude_patterns = [pattern.strip() for pattern in exclude_patterns]
        self.processing_lock_file = processing_lock_file


class FileSystemObserver:
    def __init__(self, config: FileSystemObserverConfiguration) -> None:
        self.config = config
        self._observing = False
        self._directories = config.directories_to_observe

    def is_lock_file_present(self) -> bool:
        if not self.config.processing_lock_file:
            return False
        return any((directory / self.config.processing_lock_file).exists() for directory in self._directories)

    async def observe(self) -> AsyncIterator[Set[tuple[Change, str]]]:
        self._observing = True
        directory_paths = [str(directory) for directory in self._directories]

        try:
            async for changes in awatch(
                *directory_paths,
                debounce=500,  # Wait 500ms between events to combine rapid changes
            ):
                if not self._observing:
                    break

                yield changes

        except Exception as error:
            logger.error(f"Error observing directories: {error}")
            raise
        finally:
            self._observing = False

    def stop(self) -> None:
        self._observing = False


if __name__ == "__main__":
    pass
