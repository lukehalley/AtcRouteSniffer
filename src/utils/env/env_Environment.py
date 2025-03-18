"""Environment configuration utilities.

This module provides functions to retrieve and parse environment variables
used for configuring the ATC Route Sniffer application behavior.
"""

import os
from typing import Optional

# Default block range if environment variable is not set
DEFAULT_BLOCK_RANGE = 1000


def getBlockRange() -> int:
    """Get the configured block range for transaction processing.

    Retrieves the BLOCK_RANGE environment variable which determines
    how many blocks to process in each sniffer run.

    Returns:
        int: The number of blocks to process, defaults to DEFAULT_BLOCK_RANGE
             if environment variable is not set.

    Raises:
        ValueError: If BLOCK_RANGE is set but cannot be converted to int.
    """
    block_range_str = os.getenv('BLOCK_RANGE')
    if block_range_str is None:
        return DEFAULT_BLOCK_RANGE
    return int(block_range_str)