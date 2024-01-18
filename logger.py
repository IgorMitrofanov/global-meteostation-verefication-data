# /logger.py

"""
logger.py - Logging Configuration for all classes in project. Logging is performed both in the console and in mongodb.

Main Components:
    - Logger class: Custom logger configuration class.
    - get_logger function: Function to retrieve a configured logger instance.

Usage:
    1. Import the get_logger function from this module.
    2. Call get_logger with the name of the module to get a configured logger instance.

Example:
    ```python
    from logger import get_logger

    logger = get_logger(__name__)
    logger.info('This is an information message.')
    ```

Note:
    Ensure that the constants DB_HOST, DB_NAME, and DB_LOGS_COLLECTION_NAME are properly configured in the constants module.
    The logger configuration includes both console and MongoDB handlers.

Author:
    Igor Mitrofanov

Date:
    05/12/2023
"""

import logging


from log4mongo.handlers import MongoHandler
from constants import DB_HOST, DB_NAME, DB_LOGS_COLLECTION_NAME


class Logger:
    """
    Logger class for setting up logging in the application.

    Attributes:
        - logger (logging.Logger): The logger instance for the specified module.

    Parameters:
        - logger_name (str): The name of the logger, typically the name of the module using the logger.
        - mongo_handler: An instance of the MongoHandler for logging to MongoDB.

    Methods:
        - change_logging_level(level): Changes the logging level of the logger.

    Example:
    ```python
    from log4mongo.handlers import MongoHandler
    from constants import DB_HOST, DB_NAME, DB_LOGS_COLLECTION_NAME

    mongo_handler = MongoHandler(host=DB_HOST, database_name=DB_NAME, collection=DB_LOGS_COLLECTION_NAME)
    logger = Logger(module_name='example_module', mongo_handler=mongo_handler).logger
    logger.info('This is an informational log message.')
    ```

    Note:
    Ensure the necessary constants (DB_HOST, DB_NAME, DB_LOGS_COLLECTION_NAME) are defined.
    """
    def __init__(self, logger_name, mongo_handler):
        """
        Initializes the Logger instance.

        Parameters:
            - logger_name (str): The name of the logger, typically the name of the module using the logger.
            - mongo_handler: An instance of the MongoHandler for logging to MongoDB.
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(mongo_handler)


def get_logger(module_name):
    """
    Retrieves a logger instance for the specified module.

    Parameters:
        - module_name (str): The name of the module for which the logger is requested.

    Returns:
        logging.Logger: The logger instance.
    """
    mongo_handler = MongoHandler(host=DB_HOST, database_name=DB_NAME, collection=DB_LOGS_COLLECTION_NAME) # Handler for logging
    return Logger(module_name, mongo_handler=mongo_handler
                  ).logger