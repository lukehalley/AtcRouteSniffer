from src.aws.aws_s3 import getAbiFromS3
from src.chain.utils.utils_web3 import getWeb3Instance
from src.db.querys.querys_Networks import getNetworkById
from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

def processDexInformation(dbConnection, dex, dexIndex, dexCount, cachedNetworkDetails):

    dexName = dex["name"]
    dexNetworkDbId = dex["network_id"]

    dex["router"] = dex["router"].replace("\r", "")

    if dexNetworkDbId in cachedNetworkDetails:
        dex["network_details"] = cachedNetworkDetails[dexNetworkDbId]
    else:
        dex["network_details"] = getNetworkById(dbConnection=dbConnection, networkDbId=dexNetworkDbId)
        cachedNetworkDetails[dexNetworkDbId] = dex["network_details"]

    dex["router_abi"] = getAbiFromS3(s3Key=dex["router_s3_path"])

    networkName = dex["network_details"]["name"]

    logger.info(f"[{dexIndex + 1}/{dexCount}] Processed {dexName.title()} On {networkName.title()}")

    return dex, cachedNetworkDetails


def assignDexTransactionList(dexs, dexTransactions):
    for dexTransactionList in dexTransactions:
        i = dexTransactions.index(dexTransactionList)
        dexs[i]["transactions"] = dexTransactionList
    return dexs
