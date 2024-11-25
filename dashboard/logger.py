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
import os
import logging


class MainLogger(logging.Logger):
    def __init__(self, *args, add_log_line: callable = lambda text: print(text), **kwargs):
        super(MainLogger, self).__init__(*args)
        self.add_log_line = add_log_line
        self.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

    def change_logging_level(self, level):
        self.setLevel(level)

    def bind_log_window(self, add_log_line: callable):
        self.add_log_line = add_log_line

    def warning(self, *args, **kwargs):
        super(MainLogger, self).warning(*args, **kwargs)
        if args:
            self.add_log_line(str(30) + str(args[0]))

    def info(self, *args, **kwargs):
        super(MainLogger, self).info(*args, **kwargs)
        if args:
            self.add_log_line(str(20) + str(args[0]))

    def error(self, *args, **kwargs):
        super(MainLogger, self).error(*args, **kwargs)
        if args:
            self.add_log_line(str(40) + str(args[0]))

            # DEBUG 10, INFO 20, WARNING 30, ERROR 40, CRITICAL 50


def get_logger(module_name):
    """
    Retrieves a logger instance for the specified module.

    Parameters:
        - module_name (str): The name of the module for which the logger is requested.

    Returns:
        logging.Logger: The logger instance.
    """
    logger = MainLogger(module_name)
    return logger
