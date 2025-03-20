"""AWS S3 utilities for ABI file retrieval.

This module provides functions to retrieve contract ABI files stored
in Amazon S3 for use in transaction decoding operations.
"""

import json
import os
from typing import Optional

import boto3

from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# S3 path prefix for ABI files
ABI_PATH_PREFIX = "abis"


def getAbiFromS3(s3Key: str) -> str:
    """Retrieve a contract ABI JSON from Amazon S3.

    Fetches the ABI file from the configured S3 bucket and returns it
    as a JSON string for contract interaction.

    Args:
        s3Key: The S3 object key (filename) within the abis directory.

    Returns:
        str: JSON string representation of the contract ABI.

    Raises:
        botocore.exceptions.ClientError: If the S3 object cannot be retrieved.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    full_path = f"{ABI_PATH_PREFIX}/{s3Key}"

    s3 = boto3.resource('s3')
    s3_bucket = os.getenv("S3_BUCKET")

    obj = s3.Object(s3_bucket, full_path)
    abi = json.load(obj.get()['Body'])

    logger.debug(f"Successfully retrieved ABI from S3: {full_path}")

    return json.dumps(abi)


