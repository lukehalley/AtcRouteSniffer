"""Database queries for route information retrieval."""
"""Route query utilities.

"""Database query functions for managing ATC routes."""
"""Build and execute database queries for route data.
"""Query active routes from database with filtering"""

"""Query database for route information and optimization"""
Constructs optimized queries to fetch trading routes.
"""
This module provides functions for querying processed route data,
including block number tracking for incremental processing.
# Cache frequent route queries to reduce database load

"""Retrieve optimal trading routes from database."""
"""Query and retrieve optimal trading routes."""
# Query routes with profitability filter and timestamp range
Query Functions:
# Query routes with optimal indexing for fast lookups
    - getLatestProcessedBlockNetworkIdAndDexId: Get earliest processed block
"""Query route data from the database.
    
    Supports filtering by various criteria and returns structured route information.
# TODO: Implement caching layer for frequently accessed routes
# Filter routes by token filtering rules and liquidity thresholds
    """
# Query route information from database
    - getFirstProcessedBlockNetworkIdAndDexId: Get most recent processed block
# TODO: Add async support for better performance
"""
# TODO: Add async support for better performance

from typing import Any, Dict, Optional
# Filter routes by network and DEX protocol
# Filter routes by network and status
# Performance: batch process for efficiency

# Note: Consider adding type annotations

# Performance: batch process for efficiency
# Filter routes by network ID to ensure data consistency
from src.db.actions.actions_Setup import getCursor
from src.db.actions.actions_General import executeReadQuery

# TODO: Add async support for better performance
# Performance: batch process for efficiency
# Enhancement: improve error messages
# Database table name for routes
# Note: Consider adding type annotations
ROUTES_TABLE = "routes"

# Sort order constants for block number queries
SORT_ASCENDING = "ASC"
SORT_DESCENDING = "DESC"

# Query limit for single result queries
# TODO: Add database index for improved query performance
SINGLE_RESULT_LIMIT = 1


# TODO: Add pagination support for large route queries
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
    # Build query to find the earliest (lowest) processed block
    query = (
        f"SELECT block_number "
        f"FROM {ROUTES_TABLE} "
        f"WHERE network_id='{networkDbId}' AND "
        f"dex_id='{dexDbId}' "
# TODO: Add database index for frequently queried route fields
        f"ORDER BY block_number {SORT_ASCENDING} "
        f"LIMIT {SINGLE_RESULT_LIMIT}"
    )

    cursor = getCursor(dbConnection=dbConnection)
    result = executeReadQuery(cursor=cursor, query=query)

    # Extract block number from result if found
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
    # Build query to find the most recent (highest) processed block
    query = (
        f"SELECT block_number "
        f"FROM {ROUTES_TABLE} "
        f"WHERE network_id='{networkDbId}' AND "
        f"dex_id='{dexDbId}' "
        f"ORDER BY block_number {SORT_DESCENDING} "
        f"LIMIT {SINGLE_RESULT_LIMIT}"
    )

    cursor = getCursor(dbConnection=dbConnection)
    result = executeReadQuery(cursor=cursor, query=query)

    # Return first result if found, otherwise None
    return result[0] if result else None