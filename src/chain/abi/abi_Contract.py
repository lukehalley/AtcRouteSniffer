"""Contract instance creation and caching utilities.

This module provides functions to create Web3 contract instances with
LRU caching for improved performance when interacting with the same
contracts multiple times.
"""

import json
from functools import lru_cache
from typing import Any, Dict, List, Tuple, Union

from web3 import Web3
from web3.auto import w3
from web3.contract import Contract

# Type alias for ABI format
ABIType = Union[str, List[Dict[str, Any]]]


@lru_cache(maxsize=None)
def getContract(address: str, abi: str) -> Tuple[Contract, List[Dict[str, Any]]]:
    """Create or retrieve a cached Web3 contract instance.

    Uses LRU caching to avoid recreating contract instances for the same
    address/ABI combination, improving performance for repeated calls.

    Args:
        address: The contract address (will be checksummed).
        abi: The contract ABI, either as a JSON string or parsed list.

    Returns:
        Tuple containing:
            - Contract: The Web3 contract instance.
            - List[Dict]: The parsed ABI as a list of dictionaries.

    Note:
        The cache has no size limit (maxsize=None) as contract instances
        are reused frequently and memory usage is typically low.
    """
    parsed_abi = json.loads(abi) if isinstance(abi, str) else abi
    checksum_address = Web3.toChecksumAddress(address)
    contract = w3.eth.contract(address=checksum_address, abi=parsed_abi)
    return contract, parsed_abi