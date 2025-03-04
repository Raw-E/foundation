"""
This module provides a MongoDB client using the Motor library for asynchronous MongoDB interaction.

Features:
- MongoDBClient: A class for managing MongoDB connections and operations.
- get_custom_logger: Utility function for logging.
"""

# Standard library imports
import os

# Third-party imports
from motor.motor_asyncio import AsyncIOMotorClient

# Local development package imports
from ...component import Component
from ....universal_utility_functions import get_custom_logger

logger = get_custom_logger() 

class MongoDBClient(Component):
    """
    A class used to create and manage a MongoDB client connection using Motor.

    Attributes:
    - register_on_instance_creation (bool): Indicates if the instance should be registered on creation.
    - username (str): MongoDB username for authentication.
    - password (str): MongoDB password for authentication.
    - cluster_address (str): MongoDB cluster address.
    - app_name (str): Application name for MongoDB connection.
    - _client (AsyncIOMotorClient): The MongoDB client instance.

    Methods:
    - __init__: Initializes the MongoDBClient with optional connection parameters.
    - get_client: Asynchronously retrieves or creates the MongoDB client.
    - get_collection: Asynchronously retrieves a MongoDB collection from the specified database.
    - __aenter__: Asynchronous context manager entry method.
    - __aexit__: Asynchronous context manager exit method, closes the client.
    - _construct_uri: Constructs the MongoDB URI string for connection.
    """
    def __init__(self, username=None, password=None, cluster_address=None, app_name=None):
        """
        Initializes the MongoDBClient with the specified connection parameters.

        Parameters:
        - username (str, optional): MongoDB username for authentication.
        - password (str, optional): MongoDB password for authentication.
        - cluster_address (str, optional): MongoDB cluster address.
        - app_name (str, optional): Application name for MongoDB connection.
        """
        super().__init__()
        self.username = username  # Stores the username for MongoDB authentication.
        self.password = password  # Stores the password for MongoDB authentication.
        self.cluster_address = cluster_address  # Stores the MongoDB cluster address.
        self.app_name = app_name  # Stores the application name for the MongoDB connection.

    async def get_collection(self, database_name, collection_name):
        """
        Asynchronously retrieves a MongoDB collection from the specified database.

        Parameters:
        - database_name (str): Name of the database.
        - collection_name (str): Name of the collection.

        Returns:
        - Collection: The MongoDB collection object.
        """
        database = self._client.get_database(database_name)  # Access the specified database.
        return database[collection_name]  # Return the specified collection from the database.
    
    async def _setup_client(self):
        """
        Asynchronously creates and initializes the MongoDB client.

        Returns:
        - AsyncIOMotorClient: The initialized MongoDB client instance.
        """
        uri = self._construct_uri()
        self._client = AsyncIOMotorClient(uri)
        await self._client.admin.command('ismaster')
        logger.debug(f"Initialized new MongoDB client for URI: {uri}")

    async def __aenter__(self):
        """
        Asynchronous context manager entry method.

        Returns:
        - MongoDBClient: The current instance of MongoDBClient.
        """
        await self._setup_client()
        return self  # Return the current instance of MongoDBClient.

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronous context manager exit method, closes the client.

        Parameters:
        - exc_type: Exception type.
        - exc_val: Exception value.
        - exc_tb: Exception traceback.
        """
        if self._client:  # Check if the client exists.
            self._client.close()  # Close the MongoDB client connection.
            self._client = None  # Reset the client to None.
            logger.debug("MongoDB client connection closed")  # Log the closure of the client connection.

    def _construct_uri(self) -> str:
        """
        Constructs the MongoDB URI string for connection.

        Parameters:
        - username (str, optional): MongoDB username for authentication.
        - password (str, optional): MongoDB password for authentication.
        - cluster_address (str, optional): MongoDB cluster address.
        - app_name (str, optional): Application name for MongoDB connection.

        Returns:
        - str: The constructed MongoDB URI.
        """
        username = self.username or os.getenv("MONGODB_ATLAS_USERNAME")  # Obtain the username from the parameters or environment variables.
        password = self.password or os.getenv("MONGODB_ATLAS_PASSWORD")  # Obtain the password from the parameters or environment variables.
        cluster_address = self.cluster_address or os.getenv("MONGODB_ATLAS_CLUSTER_ADDRESS")  # Obtain the cluster address from the parameters or environment variables.
        app_name = self.app_name or os.getenv("MONGODB_ATLAS_APP_NAME")  # Obtain the app name from the parameters or environment variables.

        uri = f"mongodb+srv://{username}:{password}@{cluster_address}/?retryWrites=true&w=majority&appName={app_name}"  # Construct the MongoDB URI.

        return uri  # Return the constructed URI.