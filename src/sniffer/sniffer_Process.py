"""DEX information processing and transaction assignment utilities.

This module provides functions for processing DEX information from the database
and assigning transaction lists to DEX objects for route sniffer operations.
"""

from typing import Any, Dict, List, Tuple

from src.aws.aws_s3 import getAbiFromS3
from src.chain.utils.utils_web3 import getWeb3Instance
from src.db.querys.querys_Networks import getNetworkById
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()


def processDexInformation(
    dbConnection: Any,
    dex: Dict[str, Any],
    dexIndex: int,
    dexCount: int,
    cachedNetworkDetails: Dict[int, Dict[str, Any]]
) -> Tuple[Dict[str, Any], Dict[int, Dict[str, Any]]]:
    """Process DEX information and enrich with network details and ABI.

    Retrieves network details from cache or database, fetches the router ABI
    from S3, and sanitizes the router address.

    Args:
        dbConnection: Active database connection object.
        dex: Dictionary containing DEX information from database.
        dexIndex: Current index in the DEX processing loop.
        dexCount: Total number of DEXs being processed.
        cachedNetworkDetails: Cache of previously fetched network details.

    Returns:
        Tuple containing:
            - Dict: Enriched DEX dictionary with network_details and router_abi.
            - Dict: Updated network details cache.
    """
    dexName = dex["name"]
    dexNetworkDbId = dex["network_id"]

    # Sanitize router address by removing carriage returns
    dex["router"] = dex["router"].replace("\r", "")

    # Use cached network details or fetch from database
    if dexNetworkDbId in cachedNetworkDetails:
        dex["network_details"] = cachedNetworkDetails[dexNetworkDbId]
    else:
        dex["network_details"] = getNetworkById(dbConnection=dbConnection, networkDbId=dexNetworkDbId)
        cachedNetworkDetails[dexNetworkDbId] = dex["network_details"]

    # Fetch router ABI from S3
    dex["router_abi"] = getAbiFromS3(s3Key=dex["router_s3_path"])

    networkName = dex["network_details"]["name"]

    logger.info(f"[{dexIndex + 1}/{dexCount}] Processed {dexName.title()} On {networkName.title()}")

    return dex, cachedNetworkDetails


def assignDexTransactionList(
    dexs: List[Dict[str, Any]],
    dexTransactions: List[List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """Assign transaction lists to their corresponding DEX objects.

    Maps each transaction list to its corresponding DEX by index position,
    adding a 'transactions' key to each DEX dictionary.

    Args:
        dexs: List of DEX dictionaries to receive transactions.
        dexTransactions: List of transaction lists, one per DEX.

    Returns:
        List of DEX dictionaries with 'transactions' key added.
    """
    for dexTransactionList in dexTransactions:
        i = dexTransactions.index(dexTransactionList)
        dexs[i]["transactions"] = dexTransactionList
    return dexs
