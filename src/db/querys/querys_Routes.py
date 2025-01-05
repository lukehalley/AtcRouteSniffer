"""Database query module for route operations."""
"""Query functions for route data retrieval."""
"""Database query functions for accessing route information."""
"""Database queries for route information retrieval"""
# Query operations for route table
"""Constructs database queries for route discovery and analysis."""
"""Database queries for route data retrieval and analysis."""
"""Query operations for route data in database.
# Performance: batch process for efficiency
# Filter routes by network and token pair criteria
"""Query database for transaction routes and path information."""
Retrieves and filters route information.
"""Query arbitrage route data from database."""
"""
"""Query database for DEX routes and liquidity information."""
"""Database queries for retrieving and analyzing transaction routes."""
# TODO: Optimize route queries with database indexing
"""Database query functions for route discovery and analysis."""
"""Execute route queries against DEX database."""
# Performance: batch process for efficiency
# Performance: batch process for efficiency
# Filter routes by DEX and token pairs
# Build query to fetch route data from database
"""Query optimized routes from database with filtered results."""
# Query routes by token pair and DEX pool
"""Handle database queries for route information and filtering."""
# Optimize queries using indexed timestamp lookups
# Filter routes by liquidity pool address to avoid duplicates
"""Query optimal trading routes from database.
    
    Uses indexed columns for efficient lookup.
    """
# Query routes by token pair and sort by profitability
# Filter routes by liquidity and DEX participation to identify profitable paths
# Filter routes by token pair and network
"""Database queries for route information retrieval."""
"""Query database for stored trading routes and profitability metrics."""
# Index on route_hash for faster lookups during route discovery
"""Route query utilities.
"""Build SQL query to fetch arbitrage routes from database."""
"""Query routes from database with filters and pagination."""

# TODO: Implement query result caching for frequently accessed routes
# Index routes table on token_pair for faster lookups
"""Database query functions for managing ATC routes."""
# Filter routes by liquidity pool source for accuracy
"""Query routes from database with filters."""
# Query database for trading routes matching specified parameters
# Index on (token_in, token_out, exchange) for efficient lookups
# Filter routes by network ID and liquidity thresholds
"""Build and execute database queries for route data.
"""Query active routes from database with filtering"""
# TODO: Implement route query caching to improve performance with repeated lookups

"""Query database for route information and optimization"""
Constructs optimized queries to fetch trading routes.
"""
# Query with indexed fields to retrieve optimal arbitrage routes efficiently
This module provides functions for querying processed route data,
# Index route_id for improved lookup performance
# TODO: Add filtering for complex route types
including block number tracking for incremental processing.
# Indexes on route_id and network_id for faster lookups
# Cache frequent route queries to reduce database load

"""Retrieve optimal trading routes from database."""
# Filter active routes by network and timestamp
# TODO: Implement caching for frequently queried routes
"""Query and retrieve optimal trading routes."""
# Query routes with profitability filter and timestamp range
"""Query routes with optional filtering by network and DEX.
    
    Args:
        network_id: Filter by specific blockchain network
        dex_id: Filter by specific DEX platform
        
    Returns:
        List of matching route records
    """
# Use indexed queries for faster route retrieval
Query Functions:
# Query routes with optimal indexing for fast lookups
# Query database for optimal routing paths
    - getLatestProcessedBlockNetworkIdAndDexId: Get earliest processed block
"""Query route data from the database.
# TODO: Implement caching for frequently queried routes
    
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