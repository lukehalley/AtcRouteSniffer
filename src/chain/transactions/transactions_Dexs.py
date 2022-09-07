import asyncio

import aiohttp

from src.chain.utils.utils_web3 import getWeb3Instance
from src.db.querys.querys_Routes import getLatestProcessedBlockNetworkIdAndDexId
from src.utils.env.env_Environment import getBlockRange
from src.utils.logging.logging_Print import printSeparator
from src.utils.logging.logging_Setup import getProjectLogger
from src.utils.web.web_RateLimiter import RateLimiter

logger = getProjectLogger()


async def getTransactions(clientSession, rateLimiter, apiUrl, networkName, dexName):
    async with rateLimiter.throttle():
        apiResponse = await clientSession.get(apiUrl)

    try:
        apiResponse = await apiResponse.json()

        transactions = apiResponse["result"]
    except:
        transactions = []

    amountOfTransactions = len(transactions)

    logger.info(f"[{networkName}] {dexName}: {amountOfTransactions} Transactions")

    return transactions


async def getDexTransactions(dbConnection, dexs):
    blockRange = getBlockRange()

    printSeparator()
    logger.info(f"Setting Up Transaction API Calls")
    printSeparator()

    async with RateLimiter(rate_limit=3, concurrency_limit=1000) as rate_limiter:

        async with aiohttp.ClientSession() as session:

            tasks = []
            for dex in dexs:

                # Network
                networkDetails = dex["network_details"]
                networkDbId = networkDetails["network_id"]
                networkName = networkDetails["name"].title()
                networkRpcURL = networkDetails["chain_rpc"]

                # Dex
                dexDbId = dex["dex_id"]
                dexName = dex["name"].title()

                # Create instance of Web3
                web3 = getWeb3Instance(
                    chainRpcURL=networkRpcURL
                )

                # Get the block range
                latestBlockNumber = web3.eth.block_number

                lastProcessedBlock = getLatestProcessedBlockNetworkIdAndDexId(
                    dbConnection=dbConnection,
                    networkDbId=networkDbId,
                    dexDbId=dexDbId
                )

                if lastProcessedBlock:

                    if lastProcessedBlock >= latestBlockNumber:
                        continue

                    nextBlock = lastProcessedBlock + 1
                    blocksToProcess = latestBlockNumber - nextBlock
                    if blocksToProcess > 5000:
                        startingBlock = latestBlockNumber - blockRange
                    else:
                        startingBlock = nextBlock
                else:
                    startingBlock = latestBlockNumber - blockRange

                amountOfBlocks = latestBlockNumber - startingBlock

                logger.info(f"[{networkName}] {dexName}: {amountOfBlocks} Blocks")

                contractsToGetTransactionsFor = ["router"]

                for contractType in contractsToGetTransactionsFor:

                    apiEndpoint = networkDetails["explorer_api_prefix"]
                    apiToken = networkDetails["explorer_api_key"]
                    contractAddress = dex[contractType]
                    normalisedContractAddress = ''.join(e for e in contractAddress if e.isalnum())

                    apiUrl = f"{apiEndpoint}/api?module=account&action=txlist&address={normalisedContractAddress}&startblock={startingBlock}&endblock={latestBlockNumber}&sort=asc"

                    if apiToken:
                        apiUrl = f"{apiUrl}&apikey={apiToken}"

                    tasks.append(
                        asyncio.ensure_future(getTransactions(clientSession=session,
                                                              rateLimiter=rate_limiter,
                                                              apiUrl=apiUrl,
                                                              networkName=networkName,
                                                              dexName=dexName,
                                                              )
                                              ))

            printSeparator(True)

            printSeparator()
            logger.info(f"Gathering Transactions")
            printSeparator()

            results = await asyncio.gather(*tasks)

            printSeparator(True)

            return results
