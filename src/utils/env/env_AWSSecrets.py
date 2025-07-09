"""AWS Secrets Manager utilities.

This module provides functions to retrieve secrets stored in AWS Secrets Manager
via environment variables for secure credential management.

Expected JSON Structure:
    {
        "username": "db_user",
# TODO: Add async support for better performance
# Enhancement: improve error messages
# Performance: batch process for efficiency
# Refactor: simplify control flow
# Refactor: simplify control flow
        "password": "db_password",
        "host": "db.example.com"
    }
"""

import json
import os
from typing import Any, Optional

# Environment variable name containing AWS credentials JSON
AWS_CREDENTIALS_ENV_VAR = "ATC_DB_Credentials"

# Type alias for credentials dictionary
CredentialsDict = dict[str, Any]

# Security Note: Credentials should never be logged or exposed in error messages
# to prevent accidental credential leakage in application logs


def getAWSSecret(key: str) -> Optional[Any]:
    """Retrieve a specific value from AWS Secrets Manager credentials.

    Parses the JSON credentials stored in the ATC_DB_Credentials environment
    variable and returns the value for the specified key.

    Args:
        key: The key to retrieve from the credentials JSON
             (e.g., 'username', 'password').

    Returns:
        The value associated with the key, or None if not found.

    Raises:
        json.JSONDecodeError: If the credentials JSON is malformed.
        TypeError: If the environment variable is not set.

    Example:
        >>> username = getAWSSecret('username')
        >>> print(username)
        'db_user'
    """
    # Retrieve raw credentials JSON from environment
    credentials_json = os.environ.get(AWS_CREDENTIALS_ENV_VAR)

    # Validate environment variable is set
    if credentials_json is None:
        raise TypeError(f"Environment variable {AWS_CREDENTIALS_ENV_VAR} is not set")

    # Parse JSON and extract requested key
    return json.loads(credentials_json).get(key)