# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for __init__.py of v1
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Current Project Subpackage Imports
# operation_framework
from .operation_framework.operation import Operation

# services.file_system_monitoring
from .services.file_system_monitoring import (
    FileSystemChangeProcessor,
    FileSystemChangeResponder,
    FileSystemObserver,
    FileSystemObserverConfiguration,
)

# services.logging
from .services.logging.custom_logger import CustomLogger
from .universal_utilities.concurrency_related.general_concurrency_utilities import (
    create_event_loop_in_background_thread,
)

# universal_utilities
from .universal_utilities.filesystem_related import (
    copy_file_or_directory,
    create_directory_safely,
    rename_subdirectory,
    update_text_in_files,
)
from .universal_utilities.metaclasses.singleton_metaclass import (
    ABCSingletonMetaclass,
    SingletonMetaclass,
)

# Star Exports
__all__ = [
    "ABCSingletonMetaclass",
    "FileSystemChangeProcessor",
    "FileSystemChangeResponder",
    "FileSystemObserver",
    "FileSystemObserverConfiguration",
    "Operation",
    "CustomLogger",
    "copy_file_or_directory",
    "create_directory_safely",
    "rename_subdirectory",
    "update_text_in_files",
    "create_event_loop_in_background_thread",
    "SingletonMetaclass",
]
