"""Logging configuration and setup utilities for the ATC Route Sniffer.

This module provides functions to configure and retrieve loggers with
consistent formatting across the application.
"""

import logging
import os
import sys


def setupLogging() -> logging.Logger:
    """Configure and initialize the main application logger.

    Sets up logging with timestamp, level, and message formatting.
    Output is directed to stdout for container compatibility.

    Returns:
        logging.Logger: Configured logger instance for the application.
    """
    logger = logging.getLogger("DFK-ARB")

    log_format = '%(asctime)s | %(levelname)s | %(message)s'
    dateFormat = os.environ.get("DATE_FORMAT")

    logging.basicConfig(level=logging.INFO, format=log_format,
                        stream=sys.stdout, datefmt=dateFormat)

    return logger


def getProjectLogger() -> logging.Logger:
    """Retrieve the project-specific logger instance.

    Returns:
        logging.Logger: The project logger for DFK-DEX operations.
    """
    return logging.getLogger("DFK-DEX")
