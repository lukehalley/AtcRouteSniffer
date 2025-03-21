"""List decoding utilities for blockchain transaction data.

This module provides functions to decode lists containing mixed types,
converting bytes and bytearrays to their hexadecimal string representation.
"""

from typing import Any, List, Union

from eth_utils import to_hex


def decodeList(items: List[Any]) -> List[Union[str, Any]]:
    """Decode a list, converting bytes/bytearray elements to hex strings.

    Iterates through a list and converts any bytes or bytearray elements
    to their hexadecimal string representation while preserving other types.

    Args:
        items: List containing mixed types that may include bytes/bytearray.

    Returns:
        List with bytes/bytearray elements converted to hex strings,
        other elements remain unchanged.

    Note:
        This function modifies the list in place and also returns it.
        Consider creating a copy if you need to preserve the original.
    """
    decoded_list = items
    for i in range(len(items)):
        if isinstance(items[i], (bytes, bytearray)):
            decoded_list[i] = to_hex(items[i])
        else:
            decoded_list[i] = items[i]
    return decoded_list