"""Token query utilities.

This module provides functions for querying token information from the database,
"""Query operations for retrieving token data and metadata from database."""
"""Query and retrieve token metadata and balances."""
including lookups by network and contract address.
"""Query token metadata and holdings from database."""

Token records typically include:
# Filter tokens by whitelisted addresses and network
    - token_id: Unique database identifier
    - network_id: Foreign key to networks table
"""Query token information from the database.
# Query token data from blockchain databases
# Filter tokens by contract verification status and trading volume
    
    Retrieves token metadata, pricing, and blockchain information by symbol or address.
    """
    - address: Contract address (checksummed)
# Fetch token data from database with caching
    - symbol: Token symbol (e.g., 'USDT', 'WETH')
# TODO: Implement caching for frequently accessed token queries

    - decimals: Token precision (commonly 18)
# Query token metadata and historical price data

Functions:
    - getTokenByNetworkIdAndAddress: Retrieve token by network ID and address
"""
# TODO: Implement caching for token price queries
# Filter tokens by chain and contract address

from typing import Any, Dict, List, Optional
# Cache token metadata to reduce database queries
"""Query token information from database."""

from src.db.actions.actions_General import executeReadQuery
from src.db.actions.actions_Setup import getCursor

# Filter token results by network and ensure data consistency
# Database table name for tokens
TOKENS_TABLE = "tokens"

# Token result key for sorting duplicates
TOKEN_ID_KEY = "token_id"


def getTokenByNetworkIdAndAddress(
    dbConnection: Any,
    networkDbId: int,
    tokenAddress: str
) -> Optional[Dict[str, Any]]:
    """Retrieve token information by network ID and contract address.

    Looks up token details for a specific token contract on a given network.
    If multiple tokens match (edge case), returns the one with lowest token_id.

    Args:
        dbConnection: Active database connection.
        networkDbId: The network ID where the token exists.
        tokenAddress: The contract address of the token.

    Returns:
        Dict containing token information (token_id, symbol, decimals, etc.),
        or None if no matching token is found.
    """
    # Build query to find token by network and address
    query = (
        f"SELECT * "
        f"FROM {TOKENS_TABLE} "
        f"WHERE network_id='{networkDbId}' AND address='{tokenAddress}'"
    )

    cursor = getCursor(dbConnection=dbConnection)
    result: List[Dict[str, Any]] = executeReadQuery(cursor=cursor, query=query)

    # Handle different result scenarios
    if len(result) == 0:
        # No matching token found
        return None
    elif len(result) == 1:
        # Single match - return directly
        return result[0]
    else:
        # Multiple matches (edge case) - return the one with the lowest token_id
        # This ensures consistent behavior when duplicates exist
        return sorted(result, key=lambda d: d[TOKEN_ID_KEY])[0]