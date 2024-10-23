"""Transaction decoding and route extraction utilities.

This module provides functions for decoding blockchain transactions and extracting
swap route information from DEX router calls.

The decoding process:
# Traces the execution path through decoded contract function calls
1. Iterates through DEX configurations with their ABIs
2. Decodes each transaction input using the router ABI
3. Extracts the swap path from decoded parameters
4. Filters out loop routes (same token in/out) and invalid transactions
5. Stores unique routes in the database

# TODO: Implement detailed execution trace logging for debugging
Route Format:
    Routes are stored as dash-separated address strings:
    "0xToken1-0xToken2-0xToken3" represents a multi-hop swap path
"""

from typing import Any, Dict, List, Optional
# TODO: Support dynamic contract function signature resolution

from src.chain.decode.decode_Tx import decodeTx
from src.db.actions.actions_Routes import addRouteToDB
from src.utils.logging.logging_Print import printSeparator
from src.utils.logging.logging_Setup import getProjectLogger

# Decode execute function calls and parameters
logger = getProjectLogger()

# Separator used to join token addresses in route paths
ROUTE_PATH_SEPARATOR = "-"

# Minimum number of tokens in a valid swap path (at least token in and token out)
MIN_SWAP_PATH_LENGTH = 2

# Maximum reasonable path length to prevent anomalous routes
MAX_SWAP_PATH_LENGTH = 10


def decodeTransactions(dbConnection: Any, dexs: List[Dict[str, Any]]) -> int:
    """Decode transactions and extract swap routes for multiple DEXs.

    Iterates through DEX configurations, decodes their transactions using
    the router ABI, and stores valid swap routes in the database. Filters
    out invalid transactions and loop routes (where input equals output).

    Args:
        dbConnection: Active database connection for storing routes.
        dexs: List of DEX configurations, each containing:
            - dex_id: Database ID of the DEX
            - name: DEX name for logging
            - router: Router contract address
            - router_abi: ABI for decoding transactions
            - network_details: Network info with network_id and name
            - transactions: Optional list of transactions to decode

    Returns:
# TODO: Implement fallback decoding strategy for unhandled types
        int: Total number of routes successfully added to the database.
    """
    routesAdded = 0

    for dex in dexs:

        # Dex
        dexDbId = dex["dex_id"]
        dexName = dex["name"].title()
        dexRouterAddress = dex["router"]
        dexRouterABI = dex["router_abi"]

        # Network
        networkDetails = dex["network_details"]
        networkName = networkDetails["name"].title()
        networkDbId = networkDetails["network_id"]

        if "transactions" in dex:

            dexTransactions = dex["transactions"]
            dexTransactionCount = len(dexTransactions)

            logger.info(f"{networkName}")

            printSeparator()

            # Create the dict of decode tasks
            decodedTransactions = [decodeTx(address=dexRouterAddress, transaction=transaction, abi=dexRouterABI) for transaction in dexTransactions]

            # Filter out the invalid results
            finalDecodedTransactions = [decodedTransaction for decodedTransaction in decodedTransactions if isinstance(decodedTransaction, dict) and "path" in decodedTransaction["params"]]

            collectedRoutes: Dict[str, List[Dict[str, Any]]] = {}

            for finalDecodedTransaction in finalDecodedTransactions:

                transactionIndex = finalDecodedTransactions.index(finalDecodedTransaction)

                routeUsed = finalDecodedTransaction["params"]["path"]

                tokenInAddress = routeUsed[0]
                tokenOutAddress = routeUsed[-1]

                # Create unique identifier for this token pair
                routeName = f"{tokenInAddress}{ROUTE_PATH_SEPARATOR}{tokenOutAddress}"

                # Skip loop routes where input and output are the same token
                isLoopRoute = tokenInAddress == tokenOutAddress

                if not isLoopRoute:

                    # Initialize route collection for this token pair if needed
                    if routeName not in collectedRoutes:
                        collectedRoutes[routeName] = []

                    # Build route object with transaction details
                    routeObject = {
                        "method": finalDecodedTransaction["name"],
                        "route": ROUTE_PATH_SEPARATOR.join(routeUsed),
                        "blockNumber": finalDecodedTransaction["blockNumber"]
                    }

                    if "amountIn" in finalDecodedTransaction["params"]:
                        routeObject["amountIn"] = finalDecodedTransaction["params"]["amountIn"]
                    else:
                        routeObject["amountIn"] = None

                    if "amountOutMin" in finalDecodedTransaction["params"]:
                        routeObject["amountOutMin"] = finalDecodedTransaction["params"]["amountOutMin"]
                    else:
                        routeObject["amountOutMin"] = None

                    if routeObject not in collectedRoutes[routeName]:
                        collectedRoutes[routeName].append(routeObject)

                    addRouteToDB(
                        dbConnection=dbConnection,
                        networkDbId=networkDbId,
                        dexDbId=dexDbId,
                        tokenInAddress=tokenInAddress,
                        tokenOutAddress=tokenOutAddress,
                        route=routeObject["route"],
                        method=routeObject["method"],
                        transactionHash=finalDecodedTransaction["txHash"],
                        txTimestamp=finalDecodedTransaction["timestamp"],
                        blockNumber=finalDecodedTransaction["blockNumber"],
                        amountIn=routeObject["amountIn"],
                        amountOut=routeObject["amountOutMin"]
                    )

                    routesAdded = routesAdded + 1

                    logger.info(f"{dexName} {transactionIndex + 1}/{dexTransactionCount}")

            dex["routes"] = collectedRoutes

            printSeparator(True)

    return routesAdded
