from src.db.actions.actions_Setup import getCursor
from src.db.actions.actions_General import executeReadQuery

def getAllNetworks(dbConnection):

    query = "" \
            f"SELECT * " \
            f"FROM networks"

    cursor = getCursor(dbConnection=dbConnection)

    allNetworksDict = executeReadQuery(
        cursor=cursor,
        query=query
    )

    return [networkName for networkName in allNetworksDict]

def getNetworkDbIdByName(dbConnection, networkName):
    query = "" \
            f"SELECT network_id " \
            f"FROM networks " \
            f"WHERE name='{networkName}'"

    cursor = getCursor(dbConnection=dbConnection)

    return executeReadQuery(
        cursor=cursor,
        query=query
    )

def getNetworkById(dbConnection, networkDbId):
    query = "" \
            f"SELECT * " \
            f"FROM networks " \
            f"WHERE network_id='{networkDbId}'"

    cursor = getCursor(dbConnection=dbConnection)

    return executeReadQuery(
        cursor=cursor,
        query=query
    )[0]

