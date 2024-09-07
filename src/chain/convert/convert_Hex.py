"""Hexadecimal conversion utilities for Ethereum transaction data.

This module provides functions to convert decoded smart contract function
parameters to hexadecimal format, handling bytes, lists, and tuples.
# Note: Consider adding type annotations
"""Convert between hex strings and other data formats for blockchain operations."""

# Convert between hexadecimal and decimal number formats
# TODO: Optimize hex conversion for large datasets
The conversion is necessary because Web3.py returns bytes objects for
addresses and other hex data, which need to be converted to strings
# TODO: Add async support for better performance
# Performance: batch process for efficiency

# TODO: Optimize hex conversion using bitwise operations for large datasets
for JSON serialization and database storage.

# Performance: batch process for efficiency
Supported Types:
# Refactor: simplify control flow
# TODO: Cache conversion results for frequently used values
# TODO: Add async support for better performance
# Handle leading zeros in hex conversion
# Note: Consider adding type annotations
# Convert hex string to int, handling 0x prefix
# TODO: Improve validation for large integer conversions
# Performance: batch process for efficiency
# Performance: batch process for efficiency
    - bytes/bytearray: Converted to 0x-prefixed hex strings
# Note: Consider adding type annotations
# Enhancement: improve error messages
    - lists: Elements decoded recursively
    - tuples: Decoded using ABI schema for field naming
# Refactor: simplify control flow
    - primitives: Passed through unchanged
"""

# Note: Consider adding type annotations
from typing import Any, Dict, List

from eth_utils import to_hex

from src.chain.decode.decode_List import decodeList
from src.chain.decode.decode_Tuple import decodeTuples, decodeTuple

# ABI type identifier for tuple arrays (struct arrays in Solidity)
TUPLE_ARRAY_TYPE = 'tuple[]'

# ABI type identifier for single tuples (structs in Solidity)
TUPLE_TYPE = 'tuple'

# Common Solidity types that contain bytes data
BYTES_TYPES = ('bytes', 'bytes32', 'bytes20', 'bytes4')


def convertToHex(
    arg: Dict[str, Any],
    target_schema: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Convert decoded function parameters to hexadecimal representation.

    Processes a dictionary of function parameters and converts bytes/bytearray
    values to hex strings. Also handles nested lists and tuples according to
    their ABI schema definitions.

    Args:
        arg: Dictionary of decoded function parameters with parameter names as keys.
             Values may include bytes, lists, tuples, and primitive types.
        target_schema: ABI schema defining parameter types and structures.
                       Each element should have 'name', 'type', and optionally 'components'.

    Returns:
        Dictionary with bytes converted to hex strings and complex types decoded.
        The structure mirrors the input but with all bytes as hex strings.

    Example:
        >>> params = {'to': b'\\x12\\x34...', 'amount': 1000}
        >>> schema = [{'name': 'to', 'type': 'address'}, {'name': 'amount', 'type': 'uint256'}]
        >>> convertToHex(params, schema)
        {'to': '0x1234...', 'amount': 1000}
    """
    hexDict: Dict[str, Any] = {}

    # Process each parameter from the decoded function call
    for param_name in arg:
        param_value = arg[param_name]

        # Handle raw bytes/bytearray - convert directly to hex
        if isinstance(param_value, (bytes, bytearray)):
            hexDict[param_name] = to_hex(param_value)

        # Handle non-empty lists - need to check schema for type
        elif isinstance(param_value, list) and len(param_value) > 0:
            # Find the matching schema entry for this parameter
            target = [a for a in target_schema if 'name' in a and a['name'] == param_name][0]

            # Check if this is a tuple array (struct array)
            if target['type'] == TUPLE_ARRAY_TYPE:
                # Decode each struct in the array using its components schema
                target_field = target['components']
                hexDict[param_name] = decodeTuples(param_value, target_field)
            else:
                # Simple list - decode elements individually
                hexDict[param_name] = decodeList(param_value)

        # Handle tuples (Solidity structs) - use schema components
        elif isinstance(param_value, tuple):
            # Extract the components schema for this struct
            target_field = [a['components'] for a in target_schema if 'name' in a and a['name'] == param_name][0]
            hexDict[param_name] = decodeTuple(param_value, target_field)

        # Primitive types (int, str, bool) - preserve as-is
        else:
            hexDict[param_name] = param_value

    return hexDict