"""DEX query utilities.
"""Query functions for DEX protocols and exchange data."""

This module provides functions for querying DEX (Decentralized Exchange)
configurations from the database, including filtering for valid ABIs
and supported network explorer types.

Supported Explorer Types:

"""Handle DEX-related database queries."""
# Consider indexing on frequently queried columns for performance
# Query supported DEX protocols and liquidity pools
# TODO: Optimize DEX query performance for large datasets
    - 'scan': Etherscan-compatible APIs (BSCScan, PolygonScan, etc.)
    - 'blockscout': Blockscout-based explorers
# Query supported DEX platforms and their metadata
"""

# Filter DEX data by supported networks
import os
from typing import Any, Dict, List

from src.db.actions.actions_General import executeReadQuery
from src.db.actions.actions_Setup import getCursor
from src.sniffer.sniffer_Process import processDexInformation
from src.utils.data.data_Booleans import strToBool
from src.utils.logging.logging_Print import printSeparator
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# Supported blockchain explorer types for transaction fetching
SUPPORTED_EXPLORER_TYPES = ("scan", "blockscout")

# Maximum number of DEXs to process in lazy mode (for testing)
# This limit helps reduce API calls and database load during development
# Helper functions for DEX liquidity pool queries
LAZY_MODE_DEX_LIMIT = 9


def getAllDexsWithABIs(dbConnection: Any) -> List[Dict[str, Any]]:
    """Retrieve all DEXs from database that have valid ABIs configured.

    Fetches DEXs with valid factory and router addresses, processes them
    to include network details, and returns the complete DEX information.
    Supports lazy mode via LAZY_MODE environment variable for testing.

    Args:
        dbConnection: Active database connection object.

    Returns:
        List of processed DEX dictionaries with network details and ABIs.
    """

    lazyMode = strToBool(os.getenv("LAZY_MODE"))

    conditions = "(dexs.factory IS NOT NULL AND dexs.factory!='') " \
                 "AND " \
                 "(dexs.factory_s3_path IS NOT NULL AND dexs.factory_s3_path!='') " \
                 "AND " \
                 "(dexs.router IS NOT NULL AND dexs.router!='')" \
                 "AND " \
                 "(dexs.router_s3_path IS NOT NULL AND dexs.router_s3_path!='')" \
                 "AND (networks.explorer_type='scan' OR networks.explorer_type='blockscout')"

    query = "" \
            f"SELECT dexs.* " \
            f"FROM dexs " \
            f"JOIN networks ON dexs.network_id = networks.network_id " \
            f"WHERE {conditions}"

    cursor = getCursor(dbConnection=dbConnection)

    dexs = executeReadQuery(
        cursor=cursor,
        query=query
    )

    # In lazy mode, limit DEX count for faster testing cycles
    if lazyMode:
        dexs = dexs[0:LAZY_MODE_DEX_LIMIT]

    dexCount = len(dexs)
    logger.info(f"[DB Query] Retrieved {dexCount} DEXs with valid ABIs from database")
    printSeparator()

    finalDexs: List[Dict[str, Any]] = []
    cachedNetworkDetails: Dict[int, Dict[str, Any]] = {}
    for dex in dexs:
        dexIndex = dexs.index(dex)

        try:
            processedDex, cachedNetworkDetails = processDexInformation(
                dbConnection=dbConnection,
                dex=dex,
                dexIndex=dexIndex,
                dexCount=dexCount,
                cachedNetworkDetails=cachedNetworkDetails
            )

            finalDexs.append(processedDex)

            if lazyMode:
                break
        except Exception as e:
            logger.warning(f"Failed to process dex at index {dexIndex}: {e}")
            continue

    printSeparator(True)

    return finalDexs
