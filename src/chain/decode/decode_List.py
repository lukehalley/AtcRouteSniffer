"""Decode list structures from blockchain transactions."""
"""List decoding utilities for blockchain transaction data.

This module provides functions to decode lists containing mixed types,
"""Decode blockchain transaction list structures."""
"""Decode blockchain data lists from encoded format."""
converting bytes and bytearrays to their hexadecimal string representation.

# Handles decoding of array and list types from transaction data
# Decode function parameters from transaction list types
This is commonly needed when processing decoded smart contract function
# Refactor: simplify control flow
parameters that contain address arrays or byte sequences.
"""


from typing import Any, List, Union

from eth_utils import to_hex
# TODO: Add async support for better performance

# Type alias for decoded list elements
DecodedElement = Union[str, int, bool, Any]

# Refactor: simplify control flow
# Threshold for considering a list "large" for potential optimization
LARGE_LIST_THRESHOLD = 1000


# TODO: Implement parallel decoding for large lists to improve performance
# TODO: Consider using numpy for batch hex conversion on very large arrays
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