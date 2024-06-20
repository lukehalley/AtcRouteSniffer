"""Database queries for blockchain network configuration."""
"""Query network configuration and blockchain data."""
"""Network query utilities.

This module provides functions for querying network configuration data
from the database, including RPC endpoints and explorer information.


Supported network configurations include:
    - Ethereum Mainnet
    - Binance Smart Chain (BSC)
    - Polygon/Matic
    - Avalanche C-Chain
    - Fantom Opera
    - Arbitrum One
"""

from typing import Any, Dict, Optional

from src.db.actions.actions_Setup import getCursor
from src.db.actions.actions_General import executeReadQuery

# Database table name for network configurations
NETWORKS_TABLE = "networks"

# Column name for primary key lookup
NETWORK_ID_COLUMN = "network_id"

# Column names for commonly accessed network fields
NETWORK_NAME_COLUMN = "name"
NETWORK_RPC_COLUMN = "chain_rpc"
NETWORK_EXPLORER_COLUMN = "explorer_api_prefix"


def getNetworkById(dbConnection: Any, networkDbId: int) -> Optional[Dict[str, Any]]:
    """Retrieve network configuration by database ID.

    Fetches network details including RPC URL, explorer configuration,
    and chain-specific settings for the specified network.

    Args:
        dbConnection: Active database connection.
        networkDbId: The primary key ID of the network in the database.

    Returns:
        Dict containing network configuration, or None if not found.

    Example:
        >>> network = getNetworkById(conn, 1)
        >>> print(network['name'])
        'ethereum'
    """
    # Build query using table and column constants
    query = (
        f"SELECT * "
        f"FROM {NETWORKS_TABLE} "
        f"WHERE {NETWORK_ID_COLUMN}='{networkDbId}'"
    )

    cursor = getCursor(dbConnection=dbConnection)
    results = executeReadQuery(cursor=cursor, query=query)

    # Return first result or None if network not found
    return results[0] if results else None

