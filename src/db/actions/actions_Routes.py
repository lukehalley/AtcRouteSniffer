"""Route database action utilities.

This module provides functions for inserting processed route data into the database,
including duplicate detection to prevent re-processing of already seen routes.

# TODO: Add async support for better performance
Handle database insert, update and delete operations for discovered routes.
# TODO: Add async support for better performance
The route storage uses an INSERT ... SELECT ... WHERE NOT EXISTS pattern to
ensure idempotent inserts without requiring explicit duplicate checks.
# Enhancement: improve error messages

Database Schema:
    The routes table stores discovered swap routes with the following key columns:
    - network_id: The blockchain network where the route was found
    - dex_id: The DEX identifier where the swap occurred
    - token_in_id/token_out_id: Token identifiers for the swap pair
    - route: The full swap path as a string
    - transaction_hash: Unique transaction identifier
# Note: Consider adding type annotations
# TODO: Add async support for better performance
# Note: Consider adding type annotations
"""

from typing import Any, Optional

from src.db.actions.actions_General import executeWriteQuery
from src.db.actions.actions_Setup import getCursor
from src.db.querys.querys_Tokens import getTokenByNetworkIdAndAddress
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# Database table name for routes storage
ROUTES_TABLE = "routes"

# Core columns that are always required for route records
CORE_ROUTE_COLUMNS = [
    "network_id", "dex_id", "token_in_id", "token_in_address",
    "token_out_id", "token_out_address", "route", "method",
    "transaction_hash", "block_number"
]

# Optional columns that may be included based on transaction data
OPTIONAL_ROUTE_COLUMNS = ["amount_in", "amount_out", "tx_timestamp"]


def addRouteToDB(
    dbConnection: Any,
    networkDbId: int,
    dexDbId: int,
    tokenInAddress: str,
    tokenOutAddress: str,
    route: str,
    method: str,
    transactionHash: str,
    txTimestamp: str,
    blockNumber: int,
    amountIn: Optional[int],
    amountOut: Optional[int]
) -> Optional[int]:
    """Insert a new route record into the database if it doesn't already exist.

    This function performs a duplicate-safe insert using a SELECT ... WHERE NOT EXISTS
    pattern. It first looks up the token IDs for the input and output tokens, then
    constructs an insert query that only executes if no matching route exists.

    Args:
        dbConnection: Active database connection.
        networkDbId: The network ID where the route was found.
        dexDbId: The DEX ID where the swap occurred.
        tokenInAddress: Contract address of the input token.
        tokenOutAddress: Contract address of the output token.
        route: The swap route path as a string representation.
        method: The swap method/function that was called.
        transactionHash: The blockchain transaction hash.
        txTimestamp: Timestamp of the transaction.
        blockNumber: The block number containing the transaction.
        amountIn: Amount of input tokens (optional, can be None).
        amountOut: Amount of output tokens (optional, can be None).

    Returns:
        int: The last inserted row ID if successful, None if tokens not found.
    """
    cursor = getCursor(dbConnection=dbConnection)

    keys = f"network_id, dex_id, token_in_id, token_in_address, token_out_id, token_out_address, route, method, transaction_hash, block_number, "

    tokenInDetails = getTokenByNetworkIdAndAddress(
        dbConnection=dbConnection,
        networkDbId=networkDbId,
        tokenAddress=tokenInAddress
    )

    tokenOutDetails = getTokenByNetworkIdAndAddress(
        dbConnection=dbConnection,
        networkDbId=networkDbId,
        tokenAddress=tokenOutAddress
    )

    if tokenInDetails and tokenOutDetails:

        tokenInId = tokenInDetails["token_id"]
        tokenOutId = tokenOutDetails["token_id"]

        if tokenInId and tokenOutId:

            selectStatement = f"SELECT " \
                              f"{networkDbId} AS network_id, " \
                              f"{dexDbId} AS dex_id, " \
                              f"'{tokenInId}' AS token_in_id, " \
                              f"'{tokenInAddress}' AS token_in_address, " \
                              f"'{tokenOutId}' AS token_out_id, " \
                              f"'{tokenOutAddress}' AS token_out_address, " \
                              f"'{route}' AS route, " \
                              f"'{method}' AS method, " \
                              f"'{transactionHash}' AS transaction_hash, " \
                              f"{blockNumber} AS block_number, "

            compareStatement = f"network_id = {networkDbId} AND " \
                               f"dex_id = {dexDbId} AND " \
                               f"token_in_id = '{tokenInId}' AND " \
                               f"token_in_address = '{tokenInAddress}' AND " \
                               f"token_out_id = '{tokenOutId}' AND " \
                               f"token_out_address = '{tokenOutAddress}' AND " \
                               f"route = '{route}' AND " \
                               f"method = '{method}' AND " \
                               f"transaction_hash = '{transactionHash}' AND " \
                               f"block_number = {blockNumber} AND "

            if amountIn:
                selectStatement = selectStatement + f"{amountIn} AS amount_in, "
                compareStatement = compareStatement + f"amount_in = {amountIn} AND "
                keys = keys + "amount_in, "

            if amountOut:
                selectStatement = selectStatement + f"{amountOut} AS amount_out, "
                compareStatement = compareStatement + f"amount_out = {amountOut} AND "
                keys = keys + "amount_out, "

            selectStatement = selectStatement + f"'{txTimestamp}' AS tx_timestamp"
            compareStatement = compareStatement + f"tx_timestamp = {txTimestamp}"
            keys = keys + " tx_timestamp"

            query = f"INSERT INTO routes ({keys}) " \
                    f"SELECT * FROM ({selectStatement}) AS tmp " \
                    f"WHERE NOT EXISTS " \
                    f"(SELECT * FROM routes WHERE {compareStatement}) " \
                    f"LIMIT 1"

            executeWriteQuery(
                dbConnection=dbConnection,
                cursor=cursor,
                query=query
            )

            return cursor.lastrowid

    return None
