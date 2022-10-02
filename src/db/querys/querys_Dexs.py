from src.db.actions.actions_Setup import getCursor
from src.db.actions.actions_General import executeReadQuery
from src.db.querys.querys_Networks import getNetworkById


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

    finalDexs = []
    cachedNetworkDetails = {}
    for dex in dexs:
        dex["router"] = dex["router"].replace("\r", "")

        dexNetworkDbId = dex["network_id"]
        if dexNetworkDbId in cachedNetworkDetails:
            dex["network_details"] = cachedNetworkDetails[dexNetworkDbId]
        else:
            dex["network_details"] = getNetworkById(dbConnection=dbConnection, networkDbId=dexNetworkDbId)
            cachedNetworkDetails[dexNetworkDbId] = dex["network_details"]

        finalDexs.append(dex)

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
