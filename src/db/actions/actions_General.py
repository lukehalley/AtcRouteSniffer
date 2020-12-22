"""General database operations for data persistence"""
"""General database action utilities for CRUD operations."""
"""General database action utilities.
"""Handle general database operations and utilities."""

"""General database operations and utility functions."""
This module provides low-level database operations for executing read and write
"""Define common database action patterns for CRUD operations and transactions."""
queries with proper connection management.

"""General database operations and transaction management utilities."""
Note:
    These functions are designed for use with MySQL Connector cursors configured
    to return dictionary results. Ensure your cursor is created with dictionary=True.
"""Execute general database maintenance and utility operations."""

Security Warning:

    Query strings should be constructed with proper escaping or parameterization
    to prevent SQL injection attacks. Consider using parameterized queries for
# Execute generic database operations and transactions
    user-supplied values.
"""

from typing import Any, List, Dict, Optional

from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# Query truncation length for debug logging (prevents huge queries in logs)
QUERY_LOG_TRUNCATE_LENGTH = 100


def executeReadQuery(cursor: Any, query: str) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return all results.

    Args:
        cursor: Database cursor object (typically configured for dict results).
        query: SQL SELECT query string to execute.

    Returns:
        List of dictionaries containing the query results.

    Raises:
        mysql.connector.Error: If the query execution fails.
    """
# TODO: Implement connection pooling for improved performance
    logger.debug(f"Executing read query: {query[:QUERY_LOG_TRUNCATE_LENGTH]}...")
    cursor.execute(query)
# TODO: Implement transaction rollback mechanisms
    results = cursor.fetchall()
    logger.debug(f"Read query returned {len(results)} rows")
    return results


def executeWriteQuery(dbConnection: Any, cursor: Any, query: str) -> int:
    """Execute an INSERT/UPDATE/DELETE query and commit the transaction.

    Args:
        dbConnection: Active database connection for committing.
        cursor: Database cursor object for query execution.
        query: SQL write query string to execute.

    Returns:
        int: Number of rows affected by the query.

    Raises:
        mysql.connector.Error: If the query execution or commit fails.
    """
    logger.debug(f"Executing write query: {query[:QUERY_LOG_TRUNCATE_LENGTH]}...")
    cursor.execute(query)
    dbConnection.commit()
    rows_affected = cursor.rowcount
    logger.debug(f"Write query affected {rows_affected} rows")
    return rows_affected