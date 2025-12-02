"""ATC Route Sniffer - Main Application Entry Point.

This module serves as the entry point for the ATC Route Sniffer application,
which monitors blockchain DEX transactions to extract and store swap route
information for analysis and optimization.

The sniffer performs the following operations:
1. Queries the database for DEX configurations with valid ABIs
2. Fetches recent transactions from blockchain explorers
3. Decodes transaction data to extract swap routes
4. Stores unique routes in the database for further analysis

Usage:
    python main.py

Environment Variables:
    BLOCK_RANGE: Number of blocks to process per run
    LAZY_MODE: If true, limits processing for testing
    DB_ENDPOINT: Database hostname
    DB_NAME: Database name
    S3_BUCKET: S3 bucket containing ABI files
"""

import asyncio
import time

from dotenv import load_dotenv
from retry import retry

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

@retry()
def runSniffer():

    # Log init message
    printSeparator()
    logger.info(f"ATC Route Sniffer")
    printSeparator()
    logger.info(f"Blocks: {getBlockRange()}")
    printSeparator(newLine=True)

    printSeparator()
    logger.info(f"Querying DB For Dexs w/ Networks + ABIs ")
    printSeparator()

    dbConnection = initDBConnection()
    dexs = getAllDexsWithABIs(
        dbConnection=dbConnection
    )

    dexTransactions = asyncio.run(getDexTransactions(
        dbConnection=dbConnection,
        dexs=dexs
    ))

    dexs = assignDexTransactionList(
        dexs=dexs,
        dexTransactions=dexTransactions
    )

    printSeparator()
    logger.info(f"Decoding + Uploading Routes")
    printSeparator()

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

runSniffer()