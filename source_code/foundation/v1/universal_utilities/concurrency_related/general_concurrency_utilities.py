import asyncio
import threading
from typing import Any, Awaitable, Callable, TypeVar

from ...services.logging.custom_logger import CustomLogger

logger = CustomLogger()

T = TypeVar("T")


def run_async_function_in_new_event_loop(
    async_function: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any
) -> T:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(async_function(*args, **kwargs))
    finally:
        loop.close()


def create_event_loop_in_background_thread() -> asyncio.AbstractEventLoop:
    """
    Creates a new event loop and runs it indefinitely in a dedicated background thread.

    This function is useful for components that need a dedicated event loop running in a separate thread,
    particularly when handling events that originate from different threads (like keyboard or file system events).
    The event loop is set as the event loop for the background thread, not the calling thread.

    Returns:
        asyncio.AbstractEventLoop: The created event loop, which is running in a background thread.
        Use event_loop.call_soon_threadsafe() to schedule coroutines from other threads.

    Example:
        background_loop = create_event_loop_in_background_thread()
        # Use background_loop.call_soon_threadsafe() to schedule coroutines from other threads
    """

    def run_event_loop(loop: asyncio.AbstractEventLoop) -> None:
        """Sets up and runs the event loop in the current thread."""
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        finally:
            loop.close()

    # Create a new event loop
    event_loop = asyncio.new_event_loop()

    # Create and start a dedicated thread for the event loop
    loop_thread = threading.Thread(
        target=run_event_loop,
        args=(event_loop,),
        daemon=True,  # Make thread daemon so it exits when main program exits
    )
    loop_thread.start()

    logger.info("Created and started unending event loop in background thread")
    return event_loop
