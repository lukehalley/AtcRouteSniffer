import asyncio

from dotenv import load_dotenv

from src.utils.env.env_Environment import getBlockRange

load_dotenv()

from src.chain.decode.decode_Execute import decodeTransactions
from src.chain.transactions.transactions_Blocks import getBlocksForRange
from src.sniffer.sniffer_Process import processTransactionsFromBlocks
from src.utils.logging.logging_Setup import getProjectLogger

# Set up logging
logger = getProjectLogger()

async def executeSniffer(chainName, chainRpcURL, dexName, dexRouterAddress, dexrouter_abi):

    # Create an async event loop
    loop = asyncio.get_event_loop()

    # Collect the previous n blocks from the current block eg. from block 3000 to 2900 where n = 100
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
            routeAbiStr=dexrouter_abi
        )
    )

    logger.info(f"Network: {chainName.title()} | Dex: {dexName.title()} [{len(results)} Routes] ✅")

    return chainName, dexName, results