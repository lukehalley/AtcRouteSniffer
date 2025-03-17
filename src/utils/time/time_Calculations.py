"""Time calculation and formatting utilities.

This module provides helper functions for datetime operations and
human-readable time formatting used throughout the application.
"""

from datetime import datetime
import os
from time import strftime, gmtime
from typing import Optional

# Time format string for minutes and seconds display
MIN_SEC_FORMAT = "%-M Mins %-S Secs"


def getCurrentDateTime() -> str:
    """Get the current datetime formatted according to environment settings.

    Returns:
        str: Current datetime string formatted using DATE_FORMAT env variable.
    """
    date_format = os.environ.get("DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime(date_format)


def getMinSecString(elapsed_time: float) -> str:
    """Convert elapsed time in seconds to a human-readable format.

    Args:
        elapsed_time: Time duration in seconds to format.

    Returns:
        str: Formatted string in "X Mins Y Secs" format.
    """
    return strftime(MIN_SEC_FORMAT, gmtime(elapsed_time))
