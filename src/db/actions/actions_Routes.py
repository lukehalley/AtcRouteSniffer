from src.db.actions.actions_General import executeWriteQuery
from src.db.actions.actions_Setup import getCursor
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()


def addRouteToDB(dbConnection, networkDbId, dexDbId, tokenInAddress, tokenOutAddress, route, method, transactionHash,
                 txTimestamp, blockNumber, amountIn, amountOut):
    cursor = getCursor(dbConnection=dbConnection)

    keys = f"network_id, dex_id, token_in_address, token_out_address, route, method, transaction_hash, block_number, "

    selectStatement = f"SELECT " \
                      f"{networkDbId} AS network_id, " \
                      f"{dexDbId} AS dex_id, " \
                      f"'{tokenInAddress}' AS token_in_address, " \
                      f"'{tokenOutAddress}' AS token_out_address, " \
                      f"'{route}' AS route, " \
                      f"'{method}' AS method, " \
                      f"'{transactionHash}' AS transaction_hash, " \
                      f"{blockNumber} AS block_number, "

    compareStatement = f"network_id = {networkDbId} AND " \
                       f"dex_id = {dexDbId} AND " \
                       f"token_in_address = '{tokenInAddress}' AND " \
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
