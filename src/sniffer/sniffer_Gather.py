import nest_asyncio
from dotenv import load_dotenv

from src.sniffer.sniffer_Execute import executeSniffer
from src.utils.logging.logging_Print import printSeparator
from src.utils.tasks.task_AyySync import gatherWithConcurrency

load_dotenv()

from src.utils.logging.logging_Setup import getProjectLogger

nest_asyncio.apply()

# Set up logging
logger = getProjectLogger()

def gatherData(dexsToSniff):

    # Log setup message
    printSeparator()
    logger.info(f"Gathering Data")
    printSeparator()

    # Asynchronously gather each dex's blocks
    tasks = [executeSniffer(
        chainName=dexDetail["network_details"]["name"],
        chainRpcURL=dexDetail["network_details"]["chain_rpc"],
        dexName=dexDetail["name"],
        dexRouterAddress=dexDetail["router"],
        dexrouter_abi=dexDetail["router_abi"]
    ) for dexDetail in dexsToSniff]

    gatheredData = await gatherWithConcurrency(*tasks)

    printSeparator(True)

    # Log setup message
    printSeparator()
    logger.info(f"Finished Gathering Routes For {len(dexsToSniff)} Dexs ✅")
    printSeparator()

    return gatheredData