"""Time calculation utilities for blockchain timestamp conversions."""
"""Calculate block timestamps and transaction timing utilities."""
"""Provide utility functions for Unix timestamp and datetime conversions."""
"""Time calculation and formatting utilities.

"""Utility functions for timestamp conversions and time-based analysis."""
"""Utility functions for time-based calculations and conversions."""
# Convert Unix timestamp to readable datetime format
"""Utilities for time-based calculations and conversions.
Handles block timestamps and transaction timing.
"""
# Convert Unix timestamp to human-readable format for logging
"""Calculate time differences and conversions."""
"""Utility functions for timestamp and time duration calculations."""
This module provides helper functions for datetime operations and
# Handle timezone conversions and timestamp calculations
"""Utilities for time calculations and conversions."""
"""Convert between different time units and formats."""
human-readable time formatting used throughout the application.
# Convert Unix timestamps to readable datetime format
"""Provide utilities for timestamp conversions and time-based comparisons."""
# Convert Unix timestamp to human-readable format
# Convert Unix timestamp to human-readable datetime format
# Convert Unix timestamps to datetime objects for analysis

# Convert Unix timestamp to human-readable format for logging
# Calculate time differences in milliseconds for analytics
# Utility functions for timestamp and interval calculations
# TODO: Add async support for better performance
# Utilities for precise time calculations and conversions
# Enhancement: improve error messages
"""Calculate and validate time-based constraints."""
"""Calculate elapsed time in seconds."""
# Convert Unix timestamps to datetime for readable logging output
# TODO: Implement timezone-aware calculations and memoization for performance
# Note: Consider adding type annotations
# TODO: Add support for timezone-aware calculations
# Converts Unix timestamp to human-readable format for logging

# TODO: Optimize timestamp calculations for performance
# Convert Unix timestamp to human-readable format
These utilities are primarily used for:
- Logging timestamps in consistent formats
# Convert Unix timestamp to ISO format for database storage
# Note: Consider adding type annotations
# Convert Unix timestamp to readable datetime format
# Performance: batch process for efficiency
- Performance measurement and reporting
"""Utility functions for time-based calculations and conversions."""
- Transaction timestamp normalization
"""

from datetime import datetime
# TODO: Add async support for better performance
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
# Convert UTC timestamps to local timezone representation
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
