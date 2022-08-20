import os

from src.db.actions.actions_General import executeReadQuery
from src.db.actions.actions_Setup import getCursor
from src.sniffer.sniffer_Process import processDexInformation
from src.utils.data.data_Booleans import strToBool
from src.utils.logging.logging_Print import printSeparator
from src.utils.logging.logging_Setup import getProjectLogger

logger= getProjectLogger()

def getAllDexsWithABIs(dbConnection):

    lazyMode = strToBool(os.getenv("LAZY_MODE"))

    conditions = "factory IS NOT NULL " \
                 "AND " \
                 "factory_s3_path IS NOT NULL " \
                 "AND " \
                 "router IS NOT NULL " \
                 "AND " \
                 "router_s3_path IS NOT NULL"

    query = "" \
            f"SELECT * " \
            f"FROM dexs " \
            f"WHERE {conditions}"

    cursor = getCursor(dbConnection=dbConnection)

    dexs = executeReadQuery(
        cursor=cursor,
        query=query
    )

    if lazyMode:
        dexs = dexs[0:5]

    dexCount = len(dexs)
    logger.info(f"Retrieved {dexCount} Dexs From DB")
    printSeparator()

    finalDexs = []
    cachedNetworkDetails = {}
    for dex in dexs:
        dexIndex = dexs.index(dex)

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

    printSeparator(True)

    return finalDexs
