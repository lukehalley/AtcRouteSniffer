from dotenv import load_dotenv
import nest_asyncio

from src.sniffer.sniffer_Execute import executeSniffer
from src.utils.env.env_Environment import getBlockRange
from src.utils.logging.logging_Print import printSeparator
from src.utils.tasks.task_AyySync import gatherWithConcurrency

load_dotenv()

from src.utils.logging.logging_Setup import setupLogging

nest_asyncio.apply()

# Set up logging
logger = setupLogging()

async def gatherData(dexsToSniff):

    # Log setup message
    printSeparator()
    logger.info(f"Gathering Data")
    printSeparator()

    # Asynchronously gather each dex's blocks
    tasks = [executeSniffer(
        chainName=dexDetail["chainName"],
        chainRpcURL=dexDetail["chainRpcURL"],
        dexName=dexDetail["dexName"],
        dexRouterAddress=dexDetail["dexRouterAddress"],
        dexRouterAbi=dexDetail["dexRouterAbi"]
    ) for dexDetail in dexsToSniff]

    gatheredData = await gatherWithConcurrency(*tasks)

    printSeparator(True)

    # Log setup message
    printSeparator()
    logger.info(f"Finished Gathering Routes For {len(dexsToSniff)} Dexs ✅")
    printSeparator()

    return gatheredData