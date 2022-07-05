import asyncio

from dotenv import load_dotenv

from src.utils.env.env_Environment import getBlockRange
from src.utils.tasks.task_AyySync import gatherWithConcurrency

load_dotenv()

from src.chain.decode.decode_Execute import decodeTransactions
from src.chain.transactions.transactions_Blocks import getBlocksForRange
from src.sniffer.sniffer_Process import processTransactionsFromBlocks
from src.utils.logging.logging_Setup import setupLogging

# Set up logging
logger = setupLogging()

async def executeSniffer(chainName, chainRpcURL, dexName, dexRouterAddress, dexRouterAbi):

    logger.info(chainName)

    # Collect the previous n blocks from the current block eg. from block 3000 to 2900 where n = 100
    loop = asyncio.get_event_loop()
    allBlocks, processedBlockRange = loop.run_until_complete(
        getBlocksForRange(
            chainRpcURL=chainRpcURL,
            blockRange=getBlockRange(),
            returnFullTransaction=True
        )
    )

    # Process the blocks we collected and extract and process them to get the transaction data
    processedTransactions = processTransactionsFromBlocks(
        chainRpcURL=chainRpcURL,
        blocks=allBlocks,
        dexRouterAddress=dexRouterAddress
    )

    # Create an async event loop
    loop = asyncio.get_event_loop()

    # Run the Dexscreener scraper
    results = loop.run_until_complete(
        decodeTransactions(
            blockInputs=processedTransactions,
            routeAddress=dexRouterAddress,
            routeAbiStr=dexRouterAbi
        )
    )

    return chainName, dexName, results