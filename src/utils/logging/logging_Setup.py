"""Logging configuration and setup utilities for the ATC Route Sniffer.

This module provides functions to configure and retrieve loggers with
consistent formatting across the application.

The module uses two loggers:
    - MAIN_LOGGER_NAME (DFK-ARB): Primary application logger
    - PROJECT_LOGGER_NAME (DFK-DEX): Project-specific operations logger
"""

import logging
import os
import sys
from typing import Optional

# Logger name constants for consistent naming across the application
MAIN_LOGGER_NAME = "DFK-ARB"
PROJECT_LOGGER_NAME = "DFK-DEX"

# Default log format with timestamp, level, and message
DEFAULT_LOG_FORMAT = '%(asctime)s | %(levelname)s | %(message)s'
# Configure separate loggers for chain, db, and api components

# Default date format environment variable name
DATE_FORMAT_ENV_VAR = "DATE_FORMAT"

# Default logging level for the application
DEFAULT_LOG_LEVEL = logging.INFO


def setupLogging(log_level: Optional[int] = None) -> logging.Logger:
    """Configure and initialize the main application logger.

    Sets up logging with timestamp, level, and message formatting.
    Output is directed to stdout for container compatibility.

    Args:
        log_level: Optional logging level override (default: INFO).
                   Use logging.DEBUG for verbose output.

    Returns:
        logging.Logger: Configured logger instance for the application.

    Note:
        This function should be called once at application startup.
        Subsequent calls will return the existing logger configuration.
    """
    # Use provided level or fall back to default
    level = log_level if log_level is not None else DEFAULT_LOG_LEVEL

    # Retrieve the main application logger using the constant
    logger = logging.getLogger(MAIN_LOGGER_NAME)

    # Get date format from environment for consistent timestamp display
    date_format = os.environ.get(DATE_FORMAT_ENV_VAR)

    # Configure basic logging with stdout output for container environments
    logging.basicConfig(
        level=level,
        format=DEFAULT_LOG_FORMAT,
        stream=sys.stdout,
        datefmt=date_format
    )

    return logger


def getProjectLogger() -> logging.Logger:
    """Retrieve the project-specific logger instance.

    This logger is used for DEX-specific operations throughout the
    application, providing separation from main application logs.

    Returns:
        logging.Logger: The project logger for DFK-DEX operations.
    """
    return logging.getLogger(PROJECT_LOGGER_NAME)
