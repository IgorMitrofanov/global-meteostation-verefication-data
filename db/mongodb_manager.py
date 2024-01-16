# db/mongodb_manager.py

"""
mongodb_manager.py - MongoDB Manager Module for sokolmeteo.com Statistics Tables

This module provides a MongoDBManager class, implementing the IDBManager interface,
for handling MongoDB database interactions. It uses the pymongo library for MongoDB interactions.

Main Components:
    - MongoDBManager class: Handles the connection to the MongoDB database, saves data to specified collections,
      and loads data from collections.

Usage:
    1. Import the MongoDBManager class from this module.
    2. Create an instance of MongoDBManager with appropriate MongoDB server details.
    3. Call the `save_data` method to save data to the specified collection.
    4. Call the `load_data` method to load data from the specified collection.

Example:
    ```python
    from mongodb_manager import MongoDBManager

    # Create MongoDBManager instance
    mongo_manager = MongoDBManager(db_host='your_host', db_port=27017, db_name='your_database')

    # Save data to the 'your_collection' collection
    mongo_manager.save_data(data=[{'key': 'value'}], table_name='your_collection')

    # Load data from the 'your_collection' collection for a specific upload date
    data = mongo_manager.load_data(table_name='your_collection', upload_date='2023-12-25')
    print(data)
    ```

Note:
    - Ensure that the pymongo library is installed (pip install pymongo).
    - Properly configure MongoDB server details when creating the MongoDBManager instance.

Author:
    Igor Mitrofanov
    
Date:
    05/12/2023
"""

from typing import List, Dict, Any
from datetime import datetime
from pymongo import MongoClient

from db.manager_interface import IDBManager
from db.exceptions import DocumentNotFound

from logger import get_logger


logger = get_logger(__name__)


class MongoDBManager(IDBManager):
    """
    MongoDBManager - MongoDB Manager for handling MongoDB database interactions.

    Attributes:
        - db (pymongo.database.Database): The MongoDB database instance.
    """
    def __init__(self, db_host: str, db_port: int, db_name: str) -> None:
        """
        Initializes the MongoDBManager instance.

        Parameters:
            - db_host (str): The host address of the MongoDB server.
            - db_port (int): The port number on which the MongoDB server is running.
            - db_name (str): The name of the MongoDB database.
        """
        super().__init__()
        mongo_client = MongoClient(host=db_host, port=db_port)
        self.db = mongo_client[db_name]

    def save_data(self, data: List[Dict[str, Any]], table_name: str) -> None:
        """
        Saves the provided data to the specified MongoDB collection.

        Parameters:
            - data (List[Dict[str, Any]]): The data to be saved to the collection.
            - table_name (str): The name of the MongoDB collection.

        Returns:
            None
        """
        if not data:
            logger.warning(f"Data was not received or is empty ({table_name}).")
            return

        collection = self.db[table_name]
        upload_date = datetime.now().strftime('%Y-%m-%d')
        existing_documents = collection.count_documents({'upload_date': upload_date})

        if not existing_documents:
            collection.insert_one({'upload_date': upload_date, 'data': data})
            logger.info(f"Data successfully added to the collection {table_name}, database {self.db.name}.")
        else:
            logger.warning(f"Records with the date {upload_date} already exist in the collection {table_name}.")

    def load_data(self, table_name:str, upload_date:str):
        """
        Loads data from the specified MongoDB collection for a given upload date.

        Parameters:
            - table_name (str): The name of the MongoDB collection.
            - upload_date (str): The date for which data needs to be loaded.

        Returns:
            List[Dict[str, Any]]: The loaded data from the collection.

        Raises:
            DocumentNotFound: If the document for the specified date is not found in the collection.
        """
        collection = self.db[table_name]
        query = {"upload_date": upload_date}
        result = collection.find_one(query)
        if result:
            if "data" in result:
                return result["data"]
            else:
                logger.error(f"The document from table: {table_name} with upload date: {upload_date} does not contain the data key")
        else:
            msg = f"Document from table: {table_name} with upload date: {upload_date} not found."
            raise DocumentNotFound(msg)
