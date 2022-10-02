from src.db.actions.actions_General import executeWriteQuery
from src.db.actions.actions_Setup import getCursor
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

def updateDexFactoryS3Path(dbConnection, dexDbId, contractType, s3Path):

    cursor = getCursor(dbConnection=dbConnection)

    columnName = f"{contractType}_s3_path"

    query = f"UPDATE dexs " \
            f"SET {columnName} = '{s3Path}' " \
            f"WHERE dex_id = {dexDbId};"

    executeWriteQuery(
        dbConnection=dbConnection,
        cursor=cursor,
        query=query
    )

    return cursor.lastrowid

