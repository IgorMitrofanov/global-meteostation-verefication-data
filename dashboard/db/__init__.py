# db/__init__.py

"""
__init__.py - Initialization Module for sokolmeteo.com Statistics Tables Data Module.

This module initializes the database-related components, including the database manager interface,
the MongoDB manager implementation, and custom exceptions.

Usage:
    1. Import the components from this module in other parts of the code.

Example:
    ```python
    from db import IDBManager, MongoDBManager, DocumentNotFound

    # Use the database manager interface, MongoDB manager, or custom exceptions in your code
    manager = MongoDBManager(db_host='your_host', db_port=27017, db_name='your_database')
    manager.save_data(data=[{'key': 'value'}], table_name='your_collection')

    try:
        # Your code that may raise DocumentNotFound
        raise DocumentNotFound("Document not found in the database.")
    except DocumentNotFound as e:
        print(f"Error: {e}")
    ```

Author:
    Igor Mitrofanov
    
Date:
    05/12/2023
"""

from .manager_interface import IDBManager
from .mongodb_manager import MongoDBManager
