import aio_eth

from src.chain.utils.utils_web3 import getWeb3Instance

async def getAllTransactionsForBlockRange(rpcUrl, returnFullTransaction=False, blockRange=250):

    web3 = getWeb3Instance(
        rpcUrl=rpcUrl
    )

    latestBlockNumber = web3.eth.block_number
    startingBlock = latestBlockNumber - blockRange
    async with aio_eth.EthAioAPI(rpcUrl, max_tasks=1000000) as api:
        for i in range(startingBlock, latestBlockNumber):
            api.push_task({
                "method": "eth_getBlockByNumber",
                "params": [
                    hex(i), returnFullTransaction
                ]
            })
        results = await api.exec_tasks_async()
        return results, (startingBlock, latestBlockNumber)

def getTransactionsForBlock(blockDict):
    return [transaction.hex() for transaction in blockDict["transactions"]]