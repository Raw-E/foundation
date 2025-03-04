"""
File: run_server.py

This module is responsible for configuring and running the FastAPI server using Uvicorn.

It sets up the server with the local IP address and port, then starts the Uvicorn server
with hot reloading enabled for development purposes.

Functions:
   - run_server(): Configures and starts the FastAPI server

Usage:
   python -m server.scripts.run_server

Dependencies:
   - socket
   - uvicorn
   - dotenv
   - universal_utilities (local module)

For detailed documentation, see the individual function docstrings.
"""

# Standard library imports
import os

# Third-party imports
import uvicorn
from dotenv import load_dotenv

# Local application imports

# Configuration
load_dotenv()

# Main functions
def run_server() -> None:
    """
    Configures and starts the FastAPI server using Uvicorn.

    This function performs the following steps:
    1. Retrieves the fastapi server port number from the .env file
    2. Starts the Uvicorn server with hot reloading enabled

    The server is configured to run the 'fastapi_app' from the 'backend.fastapi_app' module.
    """
    # Get the server port from the .env file, with a default of 8000 if not specified
    fastapi_server_port: int = int(os.getenv('FASTAPI_SERVER_PORT', 8000))
    
    # Start the Uvicorn server
    uvicorn.run(
        "server.fastapi_app:fastapi_app",
        host="0.0.0.0",  # Listen on all available network interfaces
        port=fastapi_server_port,
        reload=True
    )

if __name__ == "__main__":
    run_server()

# TODO: Consider adding command-line arguments for port configuration
# IDEA: Implement a graceful shutdown mechanism for the server