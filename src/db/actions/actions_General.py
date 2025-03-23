"""General database action utilities.

This module provides low-level database operations for executing read and write
queries with proper connection management.
"""

from typing import Any, List, Dict

from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()


def executeReadQuery(cursor: Any, query: str) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return all results.

    Args:
        cursor: Database cursor object (typically configured for dict results).
        query: SQL SELECT query string to execute.

    Returns:
        List of dictionaries containing the query results.
    """
    cursor.execute(query)
    return cursor.fetchall()


def executeWriteQuery(dbConnection: Any, cursor: Any, query: str) -> None:
    """Execute an INSERT/UPDATE/DELETE query and commit the transaction.

    Args:
        dbConnection: Active database connection for committing.
        cursor: Database cursor object for query execution.
        query: SQL write query string to execute.

    Returns:
        None
    """
    cursor.execute(query)
    dbConnection.commit()