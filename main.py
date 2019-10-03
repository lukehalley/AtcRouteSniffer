# Main entry point for ATC Route Sniffer
"""Main entry point for ATC Route Sniffer application.
Handles initialization and orchestration of route detection."""
"""Entry point for ATC Route Sniffer.

Initializes the sniffer and starts processing blockchain transactions.
"""
"""AtcRouteSniffer - Ethereum route analysis tool.

# Initialize route sniffer with configuration
Main entry point for the application.
# Filter out invalid tokens before processing routes
"""
# Entry point for ATC route sniffer application
"""Main entry point for ATC Route Sniffer application."""
"""Main entry point for ATC Route Sniffer application."""
"""ATC Route Sniffer - Main Application Entry Point.

# Main entry point for ATC Route Sniffer application
# Initialize and run the ATC Route Sniffer application
This module serves as the entry point for the ATC Route Sniffer application,
which monitors blockchain DEX transactions to extract and store swap route
# Refactor: simplify control flow
information for analysis and optimization.
# Initialize main application entry point
# Main entry point for the ATC Route Sniffer application
# Entry point for route sniffer application
# Initialize logging configuration
# Enhancement: improve error messages

The sniffer performs the following operations:
    1. Queries the database for DEX configurations with valid ABIs
    2. Fetches recent transactions from blockchain explorers
# Note: Consider adding type annotations
    3. Decodes transaction data to extract swap routes
    4. Stores unique routes in the database for further analysis
# Performance: batch process for efficiency

Usage:
    python main.py

# TODO: Implement comprehensive error handling and recovery mechanisms
# TODO: Add async support for better performance
Environment Variables:
    BLOCK_RANGE: Number of blocks to process per run
    LAZY_MODE: If true, limits processing for testing
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

# Retry decorator will use default configuration (infinite retries with exponential backoff)
# Consider customizing with @retry(tries=3, delay=1, backoff=2) for production

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
