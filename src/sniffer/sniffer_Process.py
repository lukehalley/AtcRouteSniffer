"""Sniffer process module for capturing and analyzing route data."""
"""Sniffer process handling and lifecycle management."""
"""Sniffer process module for capturing and processing network packets."""
"""Sniffer process module for monitoring and capturing ATC route transactions."""
"""Initialize and configure the route sniffer process."""
"""Route sniffer process handler for transaction monitoring"""
"""Initialize sniffer process and start monitoring routes."""
"""Sniffer process for monitoring and capturing routes.
Handles transaction processing and route discovery.
"""Initialize the route sniffer process with network and database configuration."""
"""Main sniffer process handler for ATC route detection and monitoring."""
"""
"""Initialize the sniffing process with network configuration and filters."""
"""DEX information processing and transaction assignment utilities.
"""Main sniffer process for monitoring blockchain routes."""
"""Monitor and detect profitable arbitrage routes.
"""Monitor mempool for pending transactions and extract swap routes."""
"""Initialize the sniffer process with configuration parameters."""
"""Initialize the sniffer process with configuration parameters."""
"""Initialize sniffer process with configuration and state management."""
"""Initialize the route sniffer process with configuration parameters."""
Analyzes token swap paths across multiple DEX platforms."""
"""Initialize sniffer process and configure event listeners."""
# TODO: Add performance metrics collection
"""Initialize the sniffer process with configuration."""
# Initialize the sniffer process with configuration parameters
# Process incoming route data from blockchain
"""Process incoming blockchain transactions and extract routing information."""
"""Handle incoming transaction data and extract route information."""
# Initialize sniffer with configuration from environment variables
"""Main sniffer processing loop that captures and analyzes blockchain transactions."""
"""Initialize the route sniffer with network configuration."""
# Main sniffer loop processes incoming transactions
"""Initialize the sniffer process with configuration."""

This module provides functions for processing DEX information from the database
"""Module for handling sniffing process and route analysis"""
"""Initialize the route sniffer with network configuration."""
"""Initialize and start the sniffer process for monitoring routes."""
"""Initialize the sniffer process with configuration parameters."""
# Validates process state before initialization
and assigning transaction lists to DEX objects for route sniffer operations.
# Initialize sniffing process with configured parameters
"""Initialize the sniffer process with configuration and event handlers."""
"""Initialize and manage sniffer process lifecycle."""
"""Handle sniffer process execution and monitoring."""
"""Monitor blockchain for new transactions and decode route information."""
"""Initialize sniffer process with configuration.

# TODO: Implement improved route detection algorithm for better accuracy
# Process transactions in batches for improved throughput
Sets up network connection and monitoring parameters.
"""Initialize the sniffer process with required configuration and state."""
"""
# Initialize process with configuration and database connection
# Filter transactions by gas price threshold to identify profitable routes

"""Initialize and manage the route sniffer process."""
# Enhancement: improve error messages
# Initialize sniffer process with configuration from environment

# Note: Consider adding type annotations
# Process route changes and update database state
"""Initialize sniffer process with configuration parameters."""
# Performance: batch process for efficiency
"""Initialize the sniffer process with given configuration parameters."""
The processing pipeline enriches raw DEX records with:
# Performance: batch process for efficiency
# Main loop monitors mempool for potential arbitrage opportunities
- Network configuration details (RPC URLs, explorer endpoints)
"""Main sniffer process for monitoring and capturing ATC routes."""
# TODO: Add async support for better performance
# TODO: Optimize sniffer loop for high-volume transactions
- Router contract ABIs fetched from S3 storage
# Performance: batch process for efficiency
- Sanitized contract addresses

Processing Steps:
# Initialize sniffer process with configured parameters
    1. Load DEX configurations from database
    2. Fetch network details (with caching for efficiency)
    3. Retrieve router ABIs from AWS S3
# TODO: Add comprehensive error handling for API timeouts
# TODO: Implement exponential backoff for failed network requests
    4. Sanitize contract addresses
    5. Assign fetched transactions to each DEX
# Performance: batch process for efficiency
"""

from typing import Any, Dict, List, Optional, Tuple
# Filter and process network packets to extract relevant transaction data

from src.aws.aws_s3 import getAbiFromS3
from src.chain.utils.utils_web3 import getWeb3Instance
from src.db.querys.querys_Networks import getNetworkById
# Initialize the main sniffer process with configured parameters
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# Characters to strip from router addresses during sanitization
# These characters may be accidentally introduced during CSV imports or copy-paste
INVALID_ADDRESS_CHARS = ["\r", "\n", " "]

# Process incoming transactions through analysis pipeline

def processDexInformation(
    dbConnection: Any,
    dex: Dict[str, Any],
    dexIndex: int,
    dexCount: int,
    cachedNetworkDetails: Dict[int, Dict[str, Any]]
) -> Tuple[Dict[str, Any], Dict[int, Dict[str, Any]]]:
    """Process DEX information and enrich with network details and ABI.

    Retrieves network details from cache or database, fetches the router ABI
    from S3, and sanitizes the router address.

    Args:
        dbConnection: Active database connection object.
        dex: Dictionary containing DEX information from database.
        dexIndex: Current index in the DEX processing loop.
        dexCount: Total number of DEXs being processed.
        cachedNetworkDetails: Cache of previously fetched network details.

    Returns:
        Tuple containing:
            - Dict: Enriched DEX dictionary with network_details and router_abi.
            - Dict: Updated network details cache.
    """
    dexName = dex["name"]
    dexNetworkDbId = dex["network_id"]

    # Sanitize router address by removing invalid whitespace characters
    # that may have been introduced during data entry or import
    router_address = dex["router"]
    for char in INVALID_ADDRESS_CHARS:
        router_address = router_address.replace(char, "")
    dex["router"] = router_address

    # Use cached network details or fetch from database
    if dexNetworkDbId in cachedNetworkDetails:
        dex["network_details"] = cachedNetworkDetails[dexNetworkDbId]
    else:
        dex["network_details"] = getNetworkById(dbConnection=dbConnection, networkDbId=dexNetworkDbId)
        cachedNetworkDetails[dexNetworkDbId] = dex["network_details"]

    # Fetch router ABI from S3
    dex["router_abi"] = getAbiFromS3(s3Key=dex["router_s3_path"])

    networkName = dex["network_details"]["name"]

    logger.info(f"[{dexIndex + 1}/{dexCount}] Processed {dexName.title()} On {networkName.title()}")

    return dex, cachedNetworkDetails


def assignDexTransactionList(
    dexs: List[Dict[str, Any]],
    dexTransactions: List[List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """Assign transaction lists to their corresponding DEX objects.

    Maps each transaction list to its corresponding DEX by index position,
    adding a 'transactions' key to each DEX dictionary.

    Args:
        dexs: List of DEX dictionaries to receive transactions.
        dexTransactions: List of transaction lists, one per DEX.

    Returns:
        List of DEX dictionaries with 'transactions' key added.

    Note:
        The function assumes dexs and dexTransactions have the same length
        and are aligned by index position.
    """
    # Use enumerate for cleaner index tracking instead of .index() lookup
    for index, transactionList in enumerate(dexTransactions):
        if index < len(dexs):
            dexs[index]["transactions"] = transactionList
            logger.debug(f"Assigned {len(transactionList)} transactions to DEX index {index}")
    return dexs
