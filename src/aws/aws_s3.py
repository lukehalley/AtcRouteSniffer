"""AWS S3 utilities for ABI file retrieval.

This module provides functions to retrieve contract ABI files stored
in Amazon S3 for use in transaction decoding operations.

ABI files are stored in the S3 bucket specified by the S3_BUCKET
environment variable, under the 'abis/' prefix.

Expected S3 Structure:
    s3://{S3_BUCKET}/abis/
        uniswap_v2_router.json
        sushiswap_router.json
        pancakeswap_router.json
        ...
"""

import json
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# S3 path prefix for ABI files within the bucket
ABI_PATH_PREFIX = "abis"

# Environment variable name for S3 bucket configuration
S3_BUCKET_ENV_VAR = "S3_BUCKET"

# Note: ABI files are typically small (~10-50KB) and fetched once per DEX
# Consider caching for high-frequency access patterns


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
        ValueError: If S3_BUCKET environment variable is not set.
    """
    # Construct full S3 object path
    full_path = f"{ABI_PATH_PREFIX}/{s3Key}"

    # Initialize S3 resource client
    s3 = boto3.resource('s3')

    # Get bucket name from environment configuration
    s3_bucket = os.getenv(S3_BUCKET_ENV_VAR)
    if not s3_bucket:
        raise ValueError(f"Environment variable {S3_BUCKET_ENV_VAR} is not set")

    # Fetch and parse the ABI file from S3
    logger.debug(f"Fetching ABI from S3: s3://{s3_bucket}/{full_path}")
    obj = s3.Object(s3_bucket, full_path)
    abi = json.load(obj.get()['Body'])

    logger.debug(f"Successfully retrieved ABI from S3: {full_path}")

    # Return as JSON string for contract initialization
    return json.dumps(abi)


