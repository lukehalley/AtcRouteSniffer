"""Tuple decoding utilities for Ethereum transaction data.

This module provides functions to recursively decode tuples from smart contract
function calls, converting bytes to hex strings and preserving the field names
from the ABI schema.
"""

from typing import Any, Dict, List, Tuple, Union

from eth_utils import to_hex


def decodeTuple(tuple_data: Tuple, target_field: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Decode a tuple into a dictionary using ABI field names.

    Recursively processes tuple elements, converting bytes to hex strings
    and nested tuples to nested dictionaries.

    Args:
        tuple_data: The tuple to decode from contract function output.
        target_field: ABI components describing the field names and types.

    Returns:
        Dict with field names as keys and decoded values.
    """
    decoded_dict: Dict[str, Any] = {}
    for i in range(len(tuple_data)):
        field_name = target_field[i]['name']
        if isinstance(tuple_data[i], (bytes, bytearray)):
            decoded_dict[field_name] = to_hex(tuple_data[i])
        elif isinstance(tuple_data[i], tuple):
            decoded_dict[field_name] = decodeTuple(tuple_data[i], target_field[i]['components'])
        else:
            decoded_dict[field_name] = tuple_data[i]
    return decoded_dict


def decodeTuples(tuple_list: List[Tuple], target_field: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Decode a list of tuples into a list of dictionaries.

    Applies decodeTuple to each element in the list.

    Args:
        tuple_list: List of tuples to decode.
        target_field: ABI components describing the field names and types.

    Returns:
        List of decoded dictionaries.
    """
    decoded_list = tuple_list
    for i in range(len(tuple_list)):
        decoded_list[i] = decodeTuple(tuple_list[i], target_field)
    return decoded_list