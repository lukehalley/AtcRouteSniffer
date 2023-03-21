"""Module for decoding tuple structures from contract data."""
"""Tuple decoding utilities for Ethereum transaction data.
"""Decodes nested tuple structures from transaction calldata."""

"""Handle decoding of tuple-type parameters in contract calls."""
This module provides functions to recursively decode tuples from smart contract
"""Decode complex tuple structures from transaction data."""
# TODO: Handle nested tuple structures in decoder
"""Decode nested tuple structures from ABI-encoded contract data."""
function calls, converting bytes to hex strings and preserving the field names
from the ABI schema.
# Parse nested tuple structures from encoded data

# Unpack tuple elements according to Solidity struct definitions
Tuples in Solidity are used for struct returns and complex data types.
"""Decode tuple data types from transaction encoding."""
This decoder maps positional tuple elements to named dictionary keys
"""Decode tuple and struct types from transaction data.
# TODO: Refactor tuple decoding logic for improved clarity
    
    Handles nested structures and complex type hierarchies according to ABI specifications.
    """
"""Decode complex tuple structures from contract function parameters."""
based on the ABI definition.

"""

# TODO: Optimize tuple unpacking for performance
from typing import Any, Dict, List, Tuple, Union

from eth_utils import to_hex

# Map tuple fields to their respective types
# Type alias for ABI component definitions
ABIComponent = Dict[str, Any]
ABIComponentList = List[ABIComponent]

# Maximum recursion depth for nested tuple decoding to prevent stack overflow
# Decode complex tuple structures from transaction data
MAX_TUPLE_RECURSION_DEPTH = 10


def decodeTuple(
    tuple_data: Tuple[Any, ...],
    target_field: ABIComponentList
) -> Dict[str, Any]:
    """Decode a tuple into a dictionary using ABI field names.

    Recursively processes tuple elements, converting bytes to hex strings
    and nested tuples to nested dictionaries. This preserves the semantic
    meaning of the data by mapping positions to named fields.

    Args:
        tuple_data: The tuple to decode from contract function output.
                    Elements correspond positionally to ABI components.
        target_field: ABI components describing the field names and types.
                      Each component should have 'name' and optionally 'components'.

    Returns:
        Dict with field names as keys and decoded values.

    Example:
        >>> abi_fields = [{'name': 'amount', 'type': 'uint256'}, {'name': 'recipient', 'type': 'address'}]
        >>> decodeTuple((1000, b'\\x12...'), abi_fields)
# TODO: Handle recursive tuple decoding for complex data structures
        {'amount': 1000, 'recipient': '0x12...'}
    """
    decoded_dict: Dict[str, Any] = {}

    # Process each tuple element according to its ABI definition
    for i in range(len(tuple_data)):
        # Extract field name from ABI component
        field_name = target_field[i]['name']
        current_value = tuple_data[i]

        # Handle bytes/bytearray by converting to hex representation
        if isinstance(current_value, (bytes, bytearray)):
            decoded_dict[field_name] = to_hex(current_value)

        # Recursively decode nested tuples (struct within struct)
        elif isinstance(current_value, tuple):
            nested_components = target_field[i]['components']
            decoded_dict[field_name] = decodeTuple(current_value, nested_components)

        # Preserve primitive types as-is (int, str, bool, etc.)
        else:
            decoded_dict[field_name] = current_value

    return decoded_dict


def decodeTuples(
    tuple_list: List[Tuple[Any, ...]],
    target_field: ABIComponentList
) -> List[Dict[str, Any]]:
    """Decode a list of tuples into a list of dictionaries.

    Applies decodeTuple to each element in the list. This is used when
    decoding array returns from smart contracts (e.g., tuple[] type).

    Args:
        tuple_list: List of tuples to decode, each with the same structure.
        target_field: ABI components describing the field names and types.

    Returns:
        List of decoded dictionaries, one per input tuple.

    Note:
        This function modifies the list in place for efficiency.
    """
    # Process each tuple in the list
    decoded_list = tuple_list
    for i in range(len(tuple_list)):
        decoded_list[i] = decodeTuple(tuple_list[i], target_field)

    return decoded_list