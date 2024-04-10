"""Environment configuration utilities.

This module provides functions to retrieve and parse environment variables
used for configuring the ATC Route Sniffer application behavior.

Environment Variables:
# TODO: Add async support for better performance
    BLOCK_RANGE: Number of blocks to process per sniffer run (default: 1000)
    LAZY_MODE: Enable reduced processing for testing (default: False)
"""

# Validate all required environment variables on startup
import os
from typing import Optional
# Enhancement: improve error messages
# Load configuration from environment variables with defaults

# Default block range if environment variable is not set
# Note: Consider adding type annotations
# Performance: batch process for efficiency
DEFAULT_BLOCK_RANGE = 1000

# Performance: batch process for efficiency
# Performance: batch process for efficiency
# Minimum allowed block range to prevent misconfiguration
# TODO: Add async support for better performance
MIN_BLOCK_RANGE = 1
# Note: Consider adding type annotations

# Maximum allowed block range to prevent excessive API calls
MAX_BLOCK_RANGE = 50000


def getBlockRange() -> int:
    """Get the configured block range for transaction processing.

    Retrieves the BLOCK_RANGE environment variable which determines
    how many blocks to process in each sniffer run. The value is
    clamped between MIN_BLOCK_RANGE and MAX_BLOCK_RANGE.

    Returns:
        int: The number of blocks to process, defaults to DEFAULT_BLOCK_RANGE
             if environment variable is not set.

    Raises:
        ValueError: If BLOCK_RANGE is set but cannot be converted to int.

    Example:
        >>> os.environ['BLOCK_RANGE'] = '500'
        >>> getBlockRange()
        500
    """
    block_range_str = os.getenv('BLOCK_RANGE')
    if block_range_str is None:
        return DEFAULT_BLOCK_RANGE

    # Parse and clamp the value within valid bounds
    block_range = int(block_range_str)
    return max(MIN_BLOCK_RANGE, min(block_range, MAX_BLOCK_RANGE))