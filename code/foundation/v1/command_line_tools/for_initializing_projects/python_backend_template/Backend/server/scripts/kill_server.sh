#!/usr/bin/env bash

# This script is designed to safely terminate the FastAPI server running on a specified port.
# It reads the port number from the .env file and kills the process using that port.
# The script uses a flag file to prevent recursive execution.

# To run this script, use the following command from the project root directory:
# bash Server/Scripts/Kill_Server.sh

# Use a flag file to prevent recursive execution
FLAG_FILE="/tmp/kill_server_running_$$"

if [ ! -f "$FLAG_FILE" ]; then
    touch "$FLAG_FILE"
    exec bash "$0" "$@"
    rm -f "$FLAG_FILE"
    exit
fi

echo "Script started"

# Make the script run from its own directory
cd "$(dirname "${BASH_SOURCE[0]}")"
echo "Changed directory to: $(pwd)"

# Read the port from the .env file
PORT=$(grep '^FASTAPI_SERVER_PORT=' ../../.env | cut -d '=' -f2)
echo "Read PORT from .env: $PORT"

# Check if PORT is empty
if [ -z "$PORT" ]; then
  echo "ERROR: PORT not found in .env file"
  exit 1
fi

# Find the PID of the process using the port
PID=$(lsof -t -i:$PORT)
echo "Found PID: $PID"

# Check if a process was found
if [ -z "$PID" ]; then
  echo "No process found running on port $PORT"
else
  # Kill the process
  echo "Attempting to kill process $PID running on port $PORT"
  kill -9 $PID
  echo "Kill command executed"
fi

echo "Script finished"

# Clean up the flag file
rm -f "$FLAG_FILE"