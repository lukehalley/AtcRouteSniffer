"""Hexadecimal conversion utilities for Ethereum transaction data.

This module provides functions to convert decoded smart contract function
parameters to hexadecimal format, handling bytes, lists, and tuples.
"""

from typing import Any, Dict, List

from eth_utils import to_hex

from src.chain.decode.decode_List import decodeList
from src.chain.decode.decode_Tuple import decodeTuples, decodeTuple


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
        target_schema: ABI schema defining parameter types and structures.

    Returns:
        Dictionary with bytes converted to hex strings and complex types decoded.
    """
    hexDict: Dict[str, Any] = {}

    for k in arg:
        if isinstance(arg[k], (bytes, bytearray)):
            hexDict[k] = to_hex(arg[k])
        elif isinstance(arg[k], list) and len(arg[k]) > 0:
            target = [a for a in target_schema if 'name' in a and a['name'] == k][0]
            if target['type'] == 'tuple[]':
                target_field = target['components']
                hexDict[k] = decodeTuples(arg[k], target_field)
            else:
                hexDict[k] = decodeList(arg[k])
        elif isinstance(arg[k], tuple):
            target_field = [a['components'] for a in target_schema if 'name' in a and a['name'] == k][0]
            hexDict[k] = decodeTuple(arg[k], target_field)
        else:
            hexDict[k] = arg[k]

    return hexDict