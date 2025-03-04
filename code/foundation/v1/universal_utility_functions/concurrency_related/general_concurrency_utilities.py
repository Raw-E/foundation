import asyncio
import threading
from ..logging_related import get_custom_logger

# Initialize a logger instance for capturing debug and error messages.
logger = get_custom_logger()  

def start_unending_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    """
    Start the provided event loop and keep it running indefinitely.
    
    Args:
        loop (asyncio.AbstractEventLoop): The event loop to be started.

    This function sets the specified event loop as the current event loop
    and runs it indefinitely. If any exception occurs during its execution,
    it logs an error message instead of printing it.
    """
    # Set the provided loop as the current event loop for the thread.
    asyncio.set_event_loop(loop)  
    try:
        # Run the loop indefinitely.
        loop.run_forever()  
    except Exception as e:
        # Log any exception that occurs during the loop's execution.
        logger.error(f"An error occurred while running the event loop: {e}")


def create_and_start_unending_event_loop() -> asyncio.AbstractEventLoop:
    """
    Create a new asynchronous event loop and start it in a separate thread.

    Returns:
        asyncio.AbstractEventLoop: The newly created event loop.

    This function creates a new event loop, starts it in a separate daemon thread,
    and ensures that the loop will not prevent the program from exiting.
    """
    # Log the start of the loop creation.
    logger.debug("Creating and starting a new event loop in a new thread.")  
    # Create a new asyncio event loop instance.
    event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    # Create a new daemon thread to run the event loop continuously.
    event_loop_thread: threading.Thread = threading.Thread(
        target=start_unending_event_loop, args=(event_loop,), daemon=True)
    # Start the newly created thread.
    event_loop_thread.start()  
    # Confirm that the event loop thread has started.
    logger.debug("Event loop thread started.")  
    # Return the event loop instance to the caller.
    return event_loop

# Previous working code:
# import asyncio  # Importing asyncio to handle asynchronous I/O operations
# import threading  # Importing threading to run the event loop in a separate thread
# 
# from ...universal_utility_functions import get_custom_logger
# 
# logger = get_custom_logger()
# 
# def start_unending_event_loop(loop: asyncio.AbstractEventLoop) -> None:
#     """
#     Sets the provided event loop as the current event loop and runs it indefinitely.
#     
#     :param loop: The event loop to be started.
#     :type loop: asyncio.AbstractEventLoop
#     """
#     asyncio.set_event_loop(loop)  # Set the provided loop as the current event loop
#     try:
#         loop.run_forever()  # Run the event loop indefinitely
#     except Exception as e:
#         # IDEA: Log the exception or handle it as needed
#         print(f"An error occurred: {e}")
# 
# def create_and_start_unending_event_loop() -> asyncio.AbstractEventLoop:
#     """
#     Creates a new event loop and runs it in a separate thread.
#     
#     :return: The created event loop.
#     :rtype: asyncio.AbstractEventLoop
#     """
#     logger.debug("Creating and starting a new event loop in a new thread.")
#     event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()  # Create a new event loop
#     event_loop_thread: threading.Thread = threading.Thread(
#         target=start_unending_event_loop, args=(event_loop,), daemon=True
#     )  # Create a new thread to run the event loop
#     event_loop_thread.start()  # Start the thread
#     logger.debug("Event loop thread started.")
#     return event_loop  # Return the event loop
# 
# # IDEA: Ensure that the returned event loop is properly managed and closed when no longer needed.