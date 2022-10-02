from src.aws.aws_s3 import getAbiFromS3
from src.db.actions.actions_Setup import getCursor
from src.db.actions.actions_General import executeReadQuery
from src.db.querys.querys_Networks import getNetworkById
from src.sniffer.sniffer_Process import processDexInformation
from src.utils.logging.logging_Print import printSeparator
from src.utils.logging.logging_Setup import getProjectLogger

logger= getProjectLogger()

def getAllDexsWithABIs(dbConnection):

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

    dexCount = len(dexs)
    logger.info(f"Retrieved {dexCount} Dexs From DB")
    printSeparator()

    dexs = dexs[0:2]

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

        # break

    printSeparator(True)

    return finalDexs


def getAllDexsForNetwork(dbConnection, networkDbId):
    query = "" \
            f"SELECT * " \
            f"FROM dexs " \
            f"WHERE network_id={networkDbId}"

    cursor = getCursor(dbConnection=dbConnection)

    dexsDict = executeReadQuery(
        cursor=cursor,
        query=query
    )

    return dexsDict
