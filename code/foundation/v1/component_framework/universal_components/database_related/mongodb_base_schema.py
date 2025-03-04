"""
File: mongodb_base_schema.py

This module provides a base schema for MongoDB documents using Pydantic.

Classes:
    - MongoDBBaseSchema: A base Pydantic model for MongoDB documents

Usage:
    from mongodb_base_schema import MongoDBBaseSchema

    class MyDocument(MongoDBBaseSchema):
        field1: str
        field2: int

    # Create a new document
    doc = MyDocument(field1="value", field2=42)

    # Access the MongoDB ObjectId
    print(doc.id)

Dependencies:
    - pydantic
    - bson

For detailed documentation, see the individual class docstrings.
"""

# Standard library imports
from typing import Annotated, Optional, Any, Dict, Union

# Third-party imports
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_serializers import PlainSerializer

# Local application imports
from ....universal_utility_functions import get_custom_logger

# Set up logging for this module
logger = get_custom_logger()

# Create a custom serializer for ObjectId
# This serializer converts ObjectId to string when the model is serialized to JSON
# It also logs the serialization process for debugging purposes
ObjectIdSerializer = PlainSerializer(
    lambda x: 
        logger.debug(f"Serializing ObjectId: {x}") or str(x),  # Log and return the string
    return_type=str, 
    when_used='json'
)

# Create a custom field type for ObjectId
# This allows us to use ObjectId in our Pydantic models while ensuring proper serialization
# ObjectIdField = Annotated[ObjectId, ObjectIdSerializer]
ObjectIdField = Annotated[Union[ObjectId, str], ObjectIdSerializer]

class MongoDBBaseSchema(BaseModel):
    """
    Base Pydantic model for MongoDB documents.

    This class provides a common structure for MongoDB documents, converting '_id' to 'id'.
    It includes methods for serialization and conversion to MongoDB-compatible format.

    Attributes:
        id (Optional[ObjectIdField]): The MongoDB document's unique identifier.

    Methods:
        to_mongodb_dict(): Converts the model to a MongoDB-compatible dictionary.

    Usage:
        class MyDocument(MongoDBBaseSchema):
            field1: str
            field2: int

        doc = MyDocument(field1="value", field2=42)
        mongo_dict = doc.to_mongodb_dict()
    """
    id: Optional[ObjectIdField] = Field(default=None)

    # Configure the model to allow population by field name and arbitrary types
    # This is necessary for working with MongoDB's ObjectId and other custom types
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},  # Ensure ObjectId is properly serialized to JSON
    )

    def __init__(self, **data):
        # Convert '_id' to 'id' if present in the input data
        # This allows seamless integration with MongoDB's default '_id' field
        if '_id' in data:
            data['id'] = data.pop('_id')
        super().__init__(**data)

    def to_mongodb_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a MongoDB-compatible dictionary.

        This method prepares the model data for insertion or update in MongoDB:
        - Excludes None values to avoid overwriting existing fields with None
        - Converts 'id' back to '_id' for MongoDB compatibility
        - Ensures 'id' is an ObjectId if it's a string

        Returns:
            Dict[str, Any]: A dictionary representation of the model suitable for MongoDB operations
        """
        # Convert the model to a dict, excluding None values and the 'id' field
        data = self.model_dump(exclude_none=True, exclude={'id'})
        
        # Add '_id' if 'id' is present and not None
        if self.id is not None:
            # Convert string id to ObjectId if necessary
            _id = ObjectId(self.id) if isinstance(self.id, str) else self.id
            data['_id'] = _id
        
        return data

    
# TODO: Add methods for common MongoDB operations (e.g., save, update, delete)
# This could include methods to directly interact with a MongoDB collection

# IDEA: Consider adding validation methods specific to MongoDB requirements
# For example, methods to ensure field names don't contain dots or start with $

# IDEA: Implement a method to generate MongoDB queries based on model fields
# This could provide a type-safe way to construct queries using the model's structure
