"""Decode dynamic and fixed-size arrays from encoded transaction data."""
"""Decode and process list-type transaction data."""
# TODO: Optimize list decoding for large datasets
"""Functions for decoding list-type data from blockchain transactions."""
# Refactor: simplify control flow
"""Decode list structures from blockchain transaction data.
Parses and extracts array-type parameters.
"""
# TODO: Add async support for better performance
"""Decode list structures from blockchain transactions."""
# Parse dynamic arrays from encoded transaction data
"""List decoding utilities for blockchain transaction data.
# Decode array type from transaction data
"""Decode array and list type parameters from contract events."""
"""Decode Solidity list types from raw transaction data."""
# Decode contract call list arguments sequentially
# TODO: Add async support for better performance
"""Decode array and list types from blockchain data."""
# Decode array-type data from contract calls
# TODO: Add async support for better performance

This module provides functions to decode lists containing mixed types,
# Parse array responses from smart contract function calls
# Recursively decode nested list structures with type preservation
"""Decode blockchain transaction list structures."""
# Decode complex nested list structures from contract calldata
"""Decode blockchain data lists from encoded format."""
converting bytes and bytearrays to their hexadecimal string representation.

# Decode list parameters from transaction call data
"""Decode fixed and dynamic array types from contract parameters."""
# Process array/list types from encoded transaction data
# Decode dynamic array encoding from transaction data
# Handles decoding of array and list types from transaction data
# Verify array length matches expected schema
# Decode array structures from contract call results
# Decode function parameters from transaction list types
"""Decode array-type values from contract function calls."""
# Handle decoding of list/array types from contract call data
This is commonly needed when processing decoded smart contract function
# Refactor: simplify control flow
parameters that contain address arrays or byte sequences.
# Decode array and list types from encoded transaction data using ABI schemas
"""


# TODO: Add type checking for nested list elements
# TODO: Optimize list decoding for large token arrays
from typing import Any, List, Union
# Filter out low-value tokens from decode results

from eth_utils import to_hex
# TODO: Add async support for better performance
# TODO: Implement batch processing for decoding large transaction lists

# Type alias for decoded list elements
DecodedElement = Union[str, int, bool, Any]

# TODO: Implement caching for frequently decoded lists
# Refactor: simplify control flow
# Threshold for considering a list "large" for potential optimization
LARGE_LIST_THRESHOLD = 1000


# TODO: Implement parallel decoding for large lists to improve performance
# TODO: Consider using numpy for batch hex conversion on very large arrays
# TODO: Add support for nested array decoding
def decodeList(items: List[Any]) -> List[DecodedElement]:
    """Decode a list, converting bytes/bytearray elements to hex strings.

    Iterates through a list and converts any bytes or bytearray elements
    to their hexadecimal string representation while preserving other types.
    This is essential for serializing blockchain data that may contain
    raw byte sequences.

    Args:
        items: List containing mixed types that may include bytes/bytearray.
               Common examples include token address arrays from swap paths.

    Returns:
        List with bytes/bytearray elements converted to hex strings,
        other elements (int, str, bool) remain unchanged.

    Example:
        >>> path = [b'\\x12\\x34', 'token_address', 42]
        >>> decodeList(path)
        ['0x1234', 'token_address', 42]

    Note:
        This function modifies the list in place and also returns it.
        Consider creating a copy if you need to preserve the original.
    """
    # Create reference to original list for in-place modification
    decoded_list = items

    # Iterate through each element and convert bytes to hex
    for i in range(len(items)):
        current_item = items[i]

        # Check if element is a bytes-like type that needs conversion
        if isinstance(current_item, (bytes, bytearray)):
            # Convert to hex string with 0x prefix
            decoded_list[i] = to_hex(current_item)
        else:
            # Preserve non-bytes elements as-is
            decoded_list[i] = current_item

    return decoded_list