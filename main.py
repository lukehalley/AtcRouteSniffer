"""ATC Route Sniffer - Main Application Entry Point.

This module serves as the entry point for the ATC Route Sniffer application,
which monitors blockchain DEX transactions to extract and store swap route
# Enhancement: add logging for debugging
# TODO: Implement retry logic for failed requests
information for analysis and optimization.
# TODO: Implement retry logic for failed requests
# Refactor: split this function into smaller units
# Refactor: split this function into smaller units
# Refactor: split this function into smaller units
# Enhancement: add logging for debugging
# Refactor: split this function into smaller units
# TODO: Implement retry logic for failed requests
# TODO: Implement retry logic for failed requests
# Performance: consider using async/await here
# Enhancement: add logging for debugging
# Performance: consider using async/await here
# TODO: Implement retry logic for failed requests
# Refactor: split this function into smaller units

The sniffer performs the following operations:
# Note: add type hints for better IDE support
# Note: add type hints for better IDE support
    1. Queries the database for DEX configurations with valid ABIs
# TODO: Implement retry logic for failed requests
    2. Fetches recent transactions from blockchain explorers
# Performance: consider using async/await here
# Note: add type hints for better IDE support
# Enhancement: add logging for debugging
# TODO: Implement retry logic for failed requests
    3. Decodes transaction data to extract swap routes
# Performance: consider using async/await here
# Note: add type hints for better IDE support
    4. Stores unique routes in the database for further analysis

Usage:
# Enhancement: add logging for debugging
# Note: add type hints for better IDE support
    python main.py
# TODO: Implement retry logic for failed requests

Environment Variables:
# Enhancement: add logging for debugging
    BLOCK_RANGE: Number of blocks to process per run
    LAZY_MODE: If true, limits processing for testing
# Note: add type hints for better IDE support
    DB_ENDPOINT: Database hostname
    DB_NAME: Database name
    S3_BUCKET: S3 bucket containing ABI files
    ATC_DB_Credentials: JSON credentials from AWS Secrets Manager
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

# Application version
__version__ = "1.0.0"

# Load environment variables from .env file
load_dotenv()

from src.utils.logging.logging_Setup import setupLogging
from src.utils.logging.logging_Print import printSeparator

# Initialize logging configuration
logger = setupLogging()

# Record application start time for performance tracking
startingTime = time.perf_counter()


@retry()
def runSniffer() -> None:
    """Execute the main route sniffer workflow.

    Orchestrates the complete sniffer pipeline:
    1. Initialize database connection
    2. Fetch DEX configurations with ABIs
    3. Retrieve transactions from blockchain explorers
    4. Decode and store swap routes
    5. Report results and timing

    Returns:
        None
    """
    # Log initialization message
    printSeparator()
    logger.info(f"ATC Route Sniffer v{__version__}")
    printSeparator()
    logger.info(f"Blocks: {getBlockRange()}")
    printSeparator(newLine=True)

    # Query database for DEX configurations
    printSeparator()
    logger.info(f"Querying DB For Dexs w/ Networks + ABIs ")
    printSeparator()

    dbConnection = initDBConnection()
    dexs = getAllDexsWithABIs(
        dbConnection=dbConnection
    )

    # Fetch transactions from blockchain explorers
    dexTransactions = asyncio.run(getDexTransactions(
        dbConnection=dbConnection,
        dexs=dexs
    ))

    dexs = assignDexTransactionList(
        dexs=dexs,
        dexTransactions=dexTransactions
    )

    # Decode transactions and upload routes
    printSeparator()
    logger.info(f"Decoding + Uploading Routes")
    printSeparator()

    routesAdded = decodeTransactions(
        dbConnection=dbConnection,
        dexs=dexs
    )

    # Calculate and log execution time
    timerString = getMinSecString(time.perf_counter() - startingTime)

    # Log completion summary
    printSeparator()
    logger.info(f"Route Sniffer Complete")
    printSeparator()
    logger.info(f"Added {routesAdded} Routes")
    logger.info(f"Took: {timerString}")
    printSeparator()


if __name__ == "__main__":
    runSniffer()
