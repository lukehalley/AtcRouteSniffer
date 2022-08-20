import asyncio
import time

from dotenv import load_dotenv

from src.chain.decode.decode_Execute import decodeTransactions
from src.chain.transactions.transactions_Dexs import getDexTransactions
from src.db.actions.actions_Setup import initDBConnection
from src.db.querys.querys_Dexs import getAllDexsWithABIs
from src.sniffer.sniffer_Process import assignDexTransactionList
from src.utils.env.env_Environment import getBlockRange

from src.utils.time.time_Calculations import getMinSecString

load_dotenv()

from src.utils.logging.logging_Setup import setupLogging
from src.utils.logging.logging_Print import printSeparator

# Set up logging
logger = setupLogging()

# Get our starting time
startingTime = time.perf_counter()

# Log init message
printSeparator()
logger.info(f"ATC Route Sniffer")
printSeparator()
logger.info(f"Blocks: {getBlockRange()}")
printSeparator(newLine=True)

printSeparator()
logger.info(f"Querying DB For Dexs w/ Networks + ABIs ")
printSeparator()

# Run the dex sniffer
dbConnection = initDBConnection()
dexs = getAllDexsWithABIs(
    dbConnection=dbConnection
)

printSeparator()
logger.info(f"Getting Dex Transactions")
printSeparator()

dexTransactions = asyncio.run(getDexTransactions(
    dexs=dexs
))

printSeparator(True)

dexs = assignDexTransactionList(
    dexs=dexs,
    dexTransactions=dexTransactions
)

routesAdded = decodeTransactions(
    dbConnection=dbConnection,
    dexs=dexs
)

# Get our ending time
timerString = getMinSecString(time.perf_counter() - startingTime)

# Log that out scraping is done
printSeparator()
logger.info(f"Route Sniffer Complete ✅")
printSeparator()
logger.info(f"Added {routesAdded} Routes")
logger.info(f"Took: {timerString}")
printSeparator()
