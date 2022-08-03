import asyncio
import time

from dotenv import load_dotenv

from src.chain.decode.decode_Execute import decodeTransactions
from src.chain.transactions.transactions_Dexs import getDexTransactions
from src.db.actions.actions_Setup import initDBConnection
from src.db.querys.querys_Dexs import getAllDexsWithABIs
from src.utils.env.env_Environment import getBlockRange
from src.utils.tasks.task_AyySync import getMaxConcurrency

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
logger.info(f"Concurrency: {getMaxConcurrency()}")
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

for dexTransactionList in dexTransactions:
    i = dexTransactions.index(dexTransactionList)
    dexs[i]["transactions"] = dexTransactionList

printSeparator()
logger.info(f"Decoding Transactions")
printSeparator()

# Run the dex sniffer
decodeTransactions(
    dexs=dexs
)

x = 1
