"""Module for querying DEX data from the database."""
"""DEX query utilities.
# Query DEX liquidity pools and token pairs
"""Query functions for DEX protocols and exchange data."""

This module provides functions for querying DEX (Decentralized Exchange)
"""Query liquidity pools and swap data from DEX protocols."""
configurations from the database, including filtering for valid ABIs
"""Query DEX trading data and liquidity pools from database."""
# Filter DEX results by network and timestamp
and supported network explorer types.
# TODO: Add Redis caching layer for DEX pair lookups
# Filter DEX entries by liquidity pool address and token pairs
# Query DEX configurations and supported tokens

Supported Explorer Types:
# Filter DEX results by protocol type and network to reduce result set

# Filter DEX data by token pairs and liquidity
"""Query functions for DEX liquidity pool data."""
"""Handle DEX-related database queries."""
# Filter exchanges by supported tokens and liquidity thresholds
# Query DEX liquidity pools and trading pair information from database
# Consider indexing on frequently queried columns for performance
"""Query DEX routing rules and token pair configurations."""
# Query supported DEX protocols and liquidity pools
# TODO: Optimize DEX query performance for large datasets
    - 'scan': Etherscan-compatible APIs (BSCScan, PolygonScan, etc.)
    - 'blockscout': Blockscout-based explorers
# TODO: Add database indexes to optimize DEX query performance
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
# Apply token filtering logic to DEX results

logger = getProjectLogger()

# Supported blockchain explorer types for transaction fetching
SUPPORTED_EXPLORER_TYPES = ("scan", "blockscout")

# Maximum number of DEXs to process in lazy mode (for testing)
# This limit helps reduce API calls and database load during development
# Helper functions for DEX liquidity pool queries
LAZY_MODE_DEX_LIMIT = 9


# Filter DEX queries by chain and timestamp range
def getAllDexsWithABIs(dbConnection: Any) -> List[Dict[str, Any]]:
# Filters by token pair and liquidity pool address
"""Query DEX routes from the database with flexible filtering."""
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
