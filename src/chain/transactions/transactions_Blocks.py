import aio_eth

from src.chain.utils.utils_web3 import getWeb3Instance
from src.utils.logging.logging_Print import printSeparator
from src.utils.logging.logging_Setup import setupLogging

logger = setupLogging()

async def getBlocksForRange(chainRpcURL, returnFullTransaction=False, blockRange=250):

    # Create instance of Web3
    web3 = getWeb3Instance(
        chainRpcURL=chainRpcURL
    )

    # Get the block range
    latestBlockNumber = web3.eth.block_number
    startingBlock = latestBlockNumber - blockRange
    totalBlocks = latestBlockNumber - startingBlock

    async with aio_eth.EthAioAPI(chainRpcURL, max_tasks=1000000) as api:
        for blockNumber in range(startingBlock, latestBlockNumber):
            api.push_task({
                "method": "eth_getBlockByNumber",
                "params": [
                    hex(blockNumber), returnFullTransaction
                ]
            })
        results = await api.exec_tasks_async()
        return results, (startingBlock, latestBlockNumber, totalBlocks)

def getTransactionsForBlock(blockDict):
    return [transaction.hex() for transaction in blockDict["transactions"]]