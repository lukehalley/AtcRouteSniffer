"""Route query utilities.

This module provides functions for querying processed route data,
including block number tracking for incremental processing.
"""

from typing import Any, Dict, Optional

from src.db.actions.actions_Setup import getCursor
from src.db.actions.actions_General import executeReadQuery


def getLatestProcessedBlockNetworkIdAndDexId(
    dbConnection: Any,
    networkDbId: int,
    dexDbId: int
) -> Optional[int]:
    """Get the earliest processed block number for a network/DEX combination.

    Used to determine where to resume processing from. Despite the name,
    this returns the LOWEST block number (earliest) in the routes table.

    Args:
        dbConnection: Active database connection.
        networkDbId: The network ID to query.
        dexDbId: The DEX ID to query.

    Returns:
        int: The lowest block number processed, or None if no routes exist.
    """
    query = (
        f"SELECT block_number "
        f"FROM routes "
        f"WHERE network_id='{networkDbId}' AND "
        f"dex_id='{dexDbId}' "
        f"ORDER BY block_number ASC "
        f"LIMIT 1"
    )

    cursor = getCursor(dbConnection=dbConnection)
    result = executeReadQuery(cursor=cursor, query=query)

    if result:
        return int(result[0]["block_number"])
    return None


def getFirstProcessedBlockNetworkIdAndDexId(
    dbConnection: Any,
    networkDbId: int,
    dexDbId: int
) -> Optional[Dict[str, Any]]:
    """Get the most recent processed block for a network/DEX combination.

    Returns the highest block number record to determine the latest
    processed point in the blockchain.

    Args:
        dbConnection: Active database connection.
        networkDbId: The network ID to query.
        dexDbId: The DEX ID to query.

    Returns:
        Dict containing block_number, or None if no routes exist.
    """
    query = (
        f"SELECT block_number "
        f"FROM routes "
        f"WHERE network_id='{networkDbId}' AND "
        f"dex_id='{dexDbId}' "
        f"ORDER BY block_number DESC "
        f"LIMIT 1"
    )

    cursor = getCursor(dbConnection=dbConnection)
    result = executeReadQuery(cursor=cursor, query=query)

    return result[0] if result else None