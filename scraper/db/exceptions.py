# db/exceptions.py

"""
exceptions.py - Custom Exceptions for sokolmeteo.com Statistics Tables Data Module.

This module defines custom exceptions that may be raised during database operations.

Main Components:
    - DocumentNotFound: Exception raised when a document is not found in the database.

Usage:
    1. Import the custom exceptions from this module.
    2. Handle these exceptions in your code where necessary.

Example:
    ```python
    from exceptions import DocumentNotFound

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

class DocumentNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
