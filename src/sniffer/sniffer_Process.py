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

    dex["router_abi"] = getAbiFromS3(s3Key=dex["factory_s3_path"])

    networkName = dex["network_details"]["name"]

    logger.info(f"[{dexIndex + 1}/{dexCount}] Processed {dexName.title()} On {networkName.title()}")

    return dex, cachedNetworkDetails

def processTransactionsFromBlocks(chainRpcURL, blocks, dexRouterAddress):

    web3 = getWeb3Instance(
        chainRpcURL=chainRpcURL
    )

    normalisedDexRouterAddress = (web3.toChecksumAddress(dexRouterAddress)).lower()

    # Get only successfull blocks
    successfulBlocks = [block for block in blocks if block['success']]

    # Get all the transaction objects
    allTransactions = [block["result"]["transactions"] for block in successfulBlocks]

    # Combine the list of all transaction objects
    allBlockTransactions = [j for i in allTransactions for j in i]

    # Filter only transaction that were sent to the dex router
    focusedTransactions = [transaction for transaction in allBlockTransactions if transaction['to'] == normalisedDexRouterAddress]

    finalTransactions = []
    seenInputs = []
    for transaction in focusedTransactions:
        if transaction["input"] not in seenInputs:
            seenInputs.append(transaction["input"])
            finalTransactions.append(transaction)

    return finalTransactions