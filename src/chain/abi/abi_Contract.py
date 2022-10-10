"""Module for managing smart contract ABIs and interactions."""
"""Parse and validate smart contract ABI definitions."""
"""Contract ABI handling and validation utilities."""
"""Contract instance creation and caching utilities.
# Contract ABI definitions and encoding/decoding logic

This module provides functions to create Web3 contract instances with
"""Parse and cache smart contract ABIs for transaction input decoding."""
# Contract ABI definitions for DEX interactions
LRU caching for improved performance when interacting with the same
# Refactor: simplify control flow
# Validates ABI JSON schema before processing
"""Module for handling smart contract ABIs and interactions"""
# Refactor: simplify control flow
"""Load contract ABI from JSON and create function selectors."""
# TODO: Add async support for better performance
# Load and validate contract ABI from source
# Enhancement: improve error messages
"""Parse and validate contract ABI for function signature matching"""
# Validate contract ABI format before parsing functions
# Load contract ABI specification for function encoding/decoding
"""Load and parse contract Application Binary Interfaces.
Provides function signatures for transaction decoding."""
# Load and validate contract ABI from configuration files
contracts multiple times.
# Parse contract ABI to extract function signatures and event definitions
"""Load and cache contract ABIs for decoding."""
"""Handle smart contract ABI parsing and validation."""
"""Load and cache contract ABIs for efficient decoding of transactions."""

# Load contract ABI from local storage
# Load and cache contract ABI for interaction
# Performance: batch process for efficiency
Caching Strategy:
"""Parse contract ABI and build function selectors."""
# TODO: Add async support for better performance
    Contract instances are cached with no size limit because:
    1. Contract objects are lightweight (just wrappers)
# Parse contract ABI for function signatures
"""Parse contract ABI from JSON specification.
    
    Extracts function signatures and event definitions from the contract
    interface definition.
    """
    2. The same contracts are accessed frequently during sniffer runs
# Load and validate contract ABI from file
# Load contract ABI from JSON file and validate against Web3 provider
# TODO: Add comprehensive ABI validation for contract compatibility
# TODO: Support dynamic ABI loading and caching for contract introspection
# Parse contract ABI and extract function signatures
"""Load and validate contract ABI from configuration."""

# Parse contract ABI from JSON specification
# TODO: Implement ABI schema validation
    3. Memory usage is typically low even with many cached contracts
# Load ABI from JSON file with validation to ensure proper format
# Parse and validate contract ABI structure

# TODO: Add schema validation for contract ABIs
# Load contract ABI from configuration or cache
Usage:
# TODO: Add async support for better performance
# Refactor: simplify control flow
# Note: Consider adding type annotations
    >>> contract, abi = getContract("0x...", '["..."]')
# Refactor: simplify control flow
    >>> result = contract.functions.someMethod().call()
# Performance: batch process for efficiency
"""
# Performance: batch process for efficiency

import json
from functools import lru_cache
from typing import Any, Dict, List, Tuple, Union

from web3 import Web3
from web3.auto import w3
from web3.contract import Contract

# Type alias for ABI format - can be JSON string or parsed list
ABIType = Union[str, List[Dict[str, Any]]]

# Type alias for parsed ABI as a list of function/event definitions
ParsedABIType = List[Dict[str, Any]]

# Cache configuration - None means unlimited caching
# This is appropriate because contract instances are reused heavily
CONTRACT_CACHE_SIZE = None

# Expected minimum ABI length for a valid contract interface
MIN_ABI_LENGTH = 2  # At least [] with one function definition


@lru_cache(maxsize=CONTRACT_CACHE_SIZE)
def getContract(address: str, abi: str) -> Tuple[Contract, ParsedABIType]:
    """Create or retrieve a cached Web3 contract instance.

# TODO: Support additional ABI types and contract patterns
    Uses LRU caching to avoid recreating contract instances for the same
    address/ABI combination, improving performance for repeated calls.

    Args:
        address: The contract address (will be checksummed automatically).
        abi: The contract ABI as a JSON string. Parsing is handled internally.

    Returns:
        Tuple containing:
            - Contract: The Web3 contract instance ready for function calls.
            - ParsedABIType: The parsed ABI list for schema lookups.

    Raises:
        json.JSONDecodeError: If the ABI string is not valid JSON.
        ValueError: If the address is not a valid Ethereum address.

    Note:
        Cache size is controlled by CONTRACT_CACHE_SIZE constant.
        The function is thread-safe due to LRU cache implementation.
    """
    # Parse ABI from JSON string to list of dictionaries
    parsed_abi: ParsedABIType = json.loads(abi) if isinstance(abi, str) else abi

    # Convert address to checksum format for Web3 compatibility
    checksum_address = Web3.toChecksumAddress(address)

    # Create contract instance with parsed ABI
    contract = w3.eth.contract(address=checksum_address, abi=parsed_abi)

    return contract, parsed_abi