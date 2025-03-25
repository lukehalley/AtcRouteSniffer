"""Token query utilities.

This module provides functions for querying token information from the database,
including lookups by network and contract address.
"""

from typing import Any, Dict, Optional

from src.db.actions.actions_General import executeReadQuery
from src.db.actions.actions_Setup import getCursor


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
    query = (
        f"SELECT * "
        f"FROM tokens "
        f"WHERE network_id='{networkDbId}' AND address='{tokenAddress}'"
    )

    cursor = getCursor(dbConnection=dbConnection)
    result = executeReadQuery(cursor=cursor, query=query)

    if len(result) == 0:
        return None
    elif len(result) == 1:
        return result[0]
    else:
        # Multiple matches - return the one with the lowest token_id
        return sorted(result, key=lambda d: d['token_id'])[0]