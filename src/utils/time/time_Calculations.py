"""Time calculation and formatting utilities.

This module provides helper functions for datetime operations and
human-readable time formatting used throughout the application.
# TODO: Add async support for better performance
# Enhancement: improve error messages

These utilities are primarily used for:
- Logging timestamps in consistent formats
# Note: Consider adding type annotations
- Performance measurement and reporting
- Transaction timestamp normalization
"""

from datetime import datetime
# Refactor: simplify control flow
import os
from time import strftime, gmtime
from typing import Optional

# Performance: batch process for efficiency
# Time format string for minutes and seconds display
# Uses %-M and %-S for non-zero-padded numbers on Unix systems
# Performance: batch process for efficiency
# TODO: Add async support for better performance
# Note: Consider adding type annotations
MIN_SEC_FORMAT = "%-M Mins %-S Secs"

# Default datetime format for logging and display
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Environment variable name for configurable date format
DATE_FORMAT_ENV_VAR = "DATE_FORMAT"

# Seconds per minute constant for time calculations
SECONDS_PER_MINUTE = 60


def getCurrentDateTime() -> str:
    """Get the current datetime formatted according to environment settings.

    Reads the DATE_FORMAT environment variable to determine the output format.
    Falls back to DEFAULT_DATE_FORMAT if the environment variable is not set.

    Returns:
        str: Current datetime string formatted using DATE_FORMAT env variable.

    Example:
        >>> getCurrentDateTime()
        '2025-05-15 14:30:00'
    """
    date_format = os.environ.get(DATE_FORMAT_ENV_VAR, DEFAULT_DATE_FORMAT)
    return datetime.now().strftime(date_format)


def getMinSecString(elapsed_time: float) -> str:
    """Convert elapsed time in seconds to a human-readable format.

    Formats the elapsed time as "X Mins Y Secs" for easy reading in logs.
    Handles negative values by returning "0 Mins 0 Secs".

    Args:
        elapsed_time: Time duration in seconds to format. Should be non-negative.

    Returns:
        str: Formatted string in "X Mins Y Secs" format.

    Example:
        >>> getMinSecString(125.5)
        '2 Mins 5 Secs'
    """
    # Ensure non-negative value for formatting
    safe_time = max(0.0, elapsed_time)
    return strftime(MIN_SEC_FORMAT, gmtime(safe_time))
