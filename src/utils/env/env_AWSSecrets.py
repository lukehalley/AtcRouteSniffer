"""AWS Secrets Manager utilities.

This module provides functions to retrieve secrets stored in AWS Secrets Manager
via environment variables for secure credential management.
"""

import json
import os
from typing import Any, Optional

# Environment variable name containing AWS credentials JSON
AWS_CREDENTIALS_ENV_VAR = "ATC_DB_Credentials"


def getAWSSecret(key: str) -> Optional[Any]:
    """Retrieve a specific value from AWS Secrets Manager credentials.

    Parses the JSON credentials stored in the ATC_DB_Credentials environment
    variable and returns the value for the specified key.

    Args:
        key: The key to retrieve from the credentials JSON (e.g., 'username', 'password').

    Returns:
        The value associated with the key, or None if not found.

    Raises:
        json.JSONDecodeError: If the credentials JSON is malformed.
        TypeError: If the environment variable is not set.
    """
    credentials_json = os.environ.get(AWS_CREDENTIALS_ENV_VAR)
    if credentials_json is None:
        raise TypeError(f"Environment variable {AWS_CREDENTIALS_ENV_VAR} is not set")
    return json.loads(credentials_json).get(key)