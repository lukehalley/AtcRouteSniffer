"""Database connection setup and management utilities.

This module provides functions for initializing MySQL database connections
using credentials from AWS Secrets Manager and environment variables.
"""

import os
from typing import Any, Optional

import mysql.connector
from mysql.connector import errorcode

from src.utils.env.env_AWSSecrets import getAWSSecret
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()


def initDBConnection():
    """Initialize a MySQL database connection using AWS credentials.

    Retrieves database credentials from AWS Secrets Manager and environment
    variables, then establishes a connection to the MySQL database.

    Returns:
        MySQLConnection: Active database connection if successful, None on error.

    Environment Variables:
        DB_ENDPOINT: The MySQL server hostname/IP.
        DB_NAME: The database name to connect to.
    """
    db_user = getAWSSecret("username")
    db_password = getAWSSecret("password")
    db_endpoint = os.getenv("DB_ENDPOINT")
    db_name = os.getenv("DB_NAME")

    try:
        db_connection = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_endpoint,
            database=db_name
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Database authentication failed: invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error(f"Database '{db_name}' does not exist")
        else:
            logger.error(f"Database connection error: {err}")
        return None
    else:
        logger.info(f"Successfully connected to database: {db_name}")
        return db_connection


def getCursor(dbConnection, dictionary=True, buffered=True):
    """Create a database cursor with the specified configuration.

    Args:
        dbConnection: Active MySQL database connection.
        dictionary: If True, return results as dictionaries. Defaults to True.
        buffered: If True, fetch all results immediately. Defaults to True.

    Returns:
        MySQLCursor: Configured cursor for executing queries.
    """
    return dbConnection.cursor(dictionary=dictionary, buffered=buffered)
