# db/manager_interface.py

"""
manager_interface.py - Database Manager Interface for sokolmeteo.com statistics tables data.

This module defines the IDBManager interface, which must be implemented by classes
that handle the storage and retrieval of parsed data.

Main Components:
    - IDBManager interface: Defines the method signatures for saving and loading data.

Usage:
    1. Import the IDBManager interface from this module.
    2. Implement the IDBManager interface in a class that handles data storage.

Example:
    ```python
    from manager_interface import IDBManager
    from typing import List, Dict, Any

    class YourDatabaseManager(IDBManager):
        def save_data(self, data: List[Dict[str, Any]], table_name: str) -> None:
            # Implement the logic to save data to your database
            pass

        def load_data(self, table_name: str, upload_date: str) -> List[Dict[str, Any]]:
            # Implement the logic to load data from your database for a given upload date
            pass
    ```

Note:
    Ensure that the implemented class provides the necessary functionality to save and load data from a specific database.
    The save_data method should handle the storage logic for the parsed data, and the load_data method should handle data retrieval.

Author:
    Igor Mitrofanov
    
Date:
    05/12/2023
"""


from typing import List, Dict, Any
from abc import ABC, abstractmethod

class IDBManager(ABC):
    @abstractmethod
    def save_data(self, data: List[Dict[str, Any]], table_name: str) -> None:
        pass

    @abstractmethod
    def load_data(self, table_name: str, upload_date: str) -> List[Dict[str, Any]]:
        pass