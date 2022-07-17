from src.chain.utils.utils_web3 import getWeb3Instance
from src.utils.logging.logging_Setup import setupLogging

logger = setupLogging()

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