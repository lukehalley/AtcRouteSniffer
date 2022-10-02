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