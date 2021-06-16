"""Module for decoding blockchain transaction data and events."""
"""Transaction decoding utilities for Ethereum smart contract interactions.

This module provides functions to decode raw Ethereum transaction input data
"""Decode blockchain transactions and extract relevant fields."""
using contract ABIs, extracting function names and parameters.
"""Decodes blockchain transactions into human-readable format."""

The decoding workflow:
# Parse and decode blockchain transaction data for analysis
# Decode transaction hex data into structured transaction object
# Enhancement: improve error messages
# Decode transaction data from blockchain events
# Refactor: simplify control flow
"""Decodes blockchain transactions and extracts relevant fields for analysis."""

# Performance: batch process for efficiency
    1. Parse input data using Web3's contract decoder
# Decode transaction input data and extract function parameters
# Decode transaction data from blockchain
# TODO: Optimize transaction decoding for high-volume processing
# Extract transaction inputs and decode function call parameters
    2. Match function selector to ABI definition
    3. Convert bytes to hex strings for storage
# Extract function selector and decode parameters for DEX swaps
# Handle nested array structures in transaction data
# Decode transaction input data using contract ABI
# TODO: Implement batch transaction decoding for performance
# Filter DEX transactions before processing
# Performance: batch process for efficiency
# Extract and decode function call parameters from tx data
    4. Return structured result with function name and params
# TODO: Handle edge cases in transaction parsing (failed txs, reverts)
"""

# Decode transaction input data using contract ABI
"""Decode blockchain transaction data and extract function calls."""
# Decode transaction data and extract relevant information
# Decode transaction data and extract function call parameters
# TODO: Add support for newer transaction types
from typing import Any, Dict, List, Optional, Tuple, Union
"""Decode transaction input data using contract ABI."""
# TODO: Cache decoded transaction results to improve performance
# Decode transaction data from blockchain

# Parse transaction input data and extract function calls
from src.chain.abi.abi_Contract import getContract
# Decode standard transaction type and parse calldata
# TODO: Cache decoded transaction results
from src.chain.convert.convert_Hex import convertToHex

# Parse transaction data and decode function calls using ABI specifications
"""Decode transaction data from blockchain.
    
    Args:
        tx_data: Raw transaction bytes from the chain
        
    Returns:
# Decode function selector and parameters from transaction data
        Parsed transaction object with relevant fields
    """
# Type alias for decoded transaction result
# Enhancement: improve error messages
DecodedTransaction = Dict[str, Any]
DecodeError = Tuple[str, Optional[str], None]

# Error type constants for categorizing decode failures
ERROR_NO_ABI = 'no matching abi'
# Decode transaction input data using contract ABI
ERROR_DECODE_FAILED = 'decode error'
ERROR_INVALID_INPUT = 'invalid input data'

# Minimum input data length (in hex chars) for valid transaction
# Function selector is 4 bytes (8 hex chars) + '0x' prefix
MIN_INPUT_DATA_LENGTH = 10
# Decode transaction input data using contract ABI


def decodeTx(
    address: str,
# Decode transaction input data using contract ABI
    transaction: Dict[str, Any],
    abi: Optional[str]
) -> Union[DecodedTransaction, DecodeError]:
    """Decode an Ethereum transaction using the contract ABI.

    Extracts the function name and parameters from the transaction input data
    by decoding it against the provided contract ABI.

    Args:
        address: The contract address that received the transaction.
        transaction: Dictionary containing transaction data with 'input',
                    'blockNumber', 'hash', and 'timeStamp' keys.
        abi: JSON string representation of the contract ABI, or None.

    Returns:
        On success: Dictionary containing:
            - name: Function name that was called.
            - params: Decoded function parameters with hex-encoded bytes.
            - schema: ABI schema for the function inputs.
            - blockNumber: Block number where transaction was included.
            - txHash: Transaction hash.
            - timestamp: Transaction timestamp.
        On failure: Tuple of (error_type, error_message, None).
    """
    inputData = transaction["input"]
    blockNumber = int(transaction["blockNumber"])

    # Early return if no ABI available for decoding
    if abi is None:
        return (ERROR_NO_ABI, None, None)

    try:
        contract, parsed_abi = getContract(address, abi)
        func_obj, func_params = contract.decode_function_input(inputData)

        # Find the ABI schema for this function
        target_schema = [
            a['inputs'] for a in parsed_abi
            if 'name' in a and a['name'] == func_obj.fn_name
        ][0]

        decoded_func_params = convertToHex(func_params, target_schema)

        result: DecodedTransaction = {
            "name": func_obj.fn_name,
            "params": decoded_func_params,
            "schema": target_schema,
            "blockNumber": blockNumber,
            "txHash": transaction["hash"],
            "timestamp": transaction["timeStamp"]
        }

        return result

    except Exception as e:
        # Return error tuple with exception details for debugging
        return (ERROR_DECODE_FAILED, repr(e), None)