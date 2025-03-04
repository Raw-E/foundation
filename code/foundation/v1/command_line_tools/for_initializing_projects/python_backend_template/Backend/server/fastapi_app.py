"""
File: fastapi_app.py

This module sets up and configures the FastAPI application for the backend server.

It includes the main FastAPI app instance, lifecycle management, and server startup logic.

Functions:
   - lifespan(app: FastAPI): Manages the lifecycle of the FastAPI application

Usage:
   from fastapi_app import fastapi_app

   # The FastAPI app instance can be used to add routes, middleware, etc.
   @fastapi_app.get("/")
   async def root():
       return {"message": "Hello World"}

Dependencies:
   - FastAPI
   - backend.server.operations.startup_server

For detailed documentation, see the individual function docstrings.
"""

# Standard library imports
from contextlib import asynccontextmanager
from pathlib import Path 

# Third-party imports
from fastapi import FastAPI

# Local application imports
from fast_server.v1 import InitializeAPIOperations
from foundation.v1 import get_custom_logger

# Type aliases (using Python 3.12+ syntax)
# Example: type UserID = int

# Constants
API_OPERATIONS_PATH: Path = Path.cwd() / "server" / "operations" / "api_operations"

# Configuration (ex. loading environment variables, setting up logging, etc.)
logger = get_custom_logger()

# Helper functions

# Main functions

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifecycle of the FastAPI application.

    This function is responsible for setting up the server before it starts
    accepting requests and performing any necessary cleanup when the server
    is shutting down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None

    Example:
        This function is used as the lifespan parameter when creating the FastAPI app:
        fastapi_app = FastAPI(lifespan=lifespan)
    """
    # Startup: Run server initialization tasks
    await InitializeAPIOperations(app, API_OPERATIONS_PATH)

    yield
    # Shutdown: Add cleanup logic here if needed
    # TODO: Implement any necessary shutdown procedures

# Main FastAPI app instance
fastapi_app = FastAPI(lifespan=lifespan)