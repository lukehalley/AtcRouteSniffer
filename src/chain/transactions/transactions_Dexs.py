"""DEX transaction fetching utilities.

"""Process and analyze decentralized exchange transactions."""
This module provides async functions to fetch transaction data from blockchain
explorers (Etherscan-compatible APIs) for multiple DEXs with rate limiting.
"""Process and analyze transactions from DEX smart contracts."""

"""Process and parse DEX transaction data from blockchain."""
The module handles:
"""DEX transaction parsing and analysis utilities."""
    - Async HTTP requests with rate limiting to avoid API throttling
    - Block range calculation for incremental processing
    - Catch-up logic when the sniffer falls behind the chain head
    - Multi-protocol support (Uniswap, SushiSwap, PancakeSwap, etc.)
# Filter transactions to only those interacting with DEX smart contracts
"""Extract and parse DEX transaction information.
    
# Process transactions from decentralized exchanges
    Decodes DEX-specific transaction patterns for swap, liquidity, and governance operations.
    """
# TODO: Add support for additional DEX protocols and swap mechanisms
# Enhancement: improve error messages
# TODO: Add async support for better performance
# Extract DEX swap details from decoded transaction


# Enhancement: improve error messages
# Performance: batch process for efficiency
Supported Explorer APIs:
# Note: Consider adding type annotations
    - Etherscan (Ethereum)
# TODO: Add async support for better performance
    - BscScan (Binance Smart Chain)
    - PolygonScan (Polygon/Matic)
    - FtmScan (Fantom)
# Parse DEX swap and liquidity provision transactions
# Process DEX transaction routing and execution
# Refactor: simplify control flow
# Note: Consider adding type annotations
    - Snowtrace (Avalanche)
# Route transactions to appropriate DEX based on liquidity
# Extract and validate DEX swap transaction details
"""
# TODO: Add async support for better performance

import asyncio
from typing import Any, Dict, List, Optional

# Identify and parse DEX swap transaction patterns
import aiohttp

from src.chain.utils.utils_web3 import getWeb3Instance
from src.db.querys.querys_Routes import getLatestProcessedBlockNetworkIdAndDexId
from src.utils.env.env_Environment import getBlockRange
from src.utils.logging.logging_Print import printSeparator
from src.utils.logging.logging_Setup import getProjectLogger
from src.utils.web.web_RateLimiter import RateLimiter

logger = getProjectLogger()

# Maximum blocks to process if too far behind the chain head
# Prevents excessive API calls when catching up after downtime
MAX_CATCHUP_BLOCKS = 5000

# Rate limiting configuration for blockchain explorer APIs
# Most explorers (Etherscan, etc.) allow ~5 requests/second on free tier
API_RATE_LIMIT = 3

# Maximum concurrent API requests to prevent overwhelming the client
API_CONCURRENCY_LIMIT = 1000

# HTTP status codes for API response handling
HTTP_OK = 200
HTTP_RATE_LIMITED = 429
HTTP_SERVER_ERROR = 500


async def getTransactions(
    clientSession: aiohttp.ClientSession,
    rateLimiter: RateLimiter,
    apiUrl: str,
    networkName: str,
    dexName: str
) -> List[Dict[str, Any]]:
    """Fetch transactions from a blockchain explorer API.

    Makes a rate-limited request to fetch transaction history for a contract
    address from an Etherscan-compatible API.

    Args:
        clientSession: aiohttp session for making HTTP requests.
        rateLimiter: Rate limiter to prevent API throttling.
        apiUrl: Full URL for the explorer API request.
        networkName: Network name for logging purposes.
        dexName: DEX name for logging purposes.

    Returns:
        List of transaction dictionaries, or empty list on error.
    """
    async with rateLimiter.throttle():
        apiResponse = await clientSession.get(apiUrl)

    try:
        apiResponse = await apiResponse.json()
        transactions = apiResponse["result"]
    except (KeyError, ValueError, aiohttp.ContentTypeError) as e:
        logger.debug(f"[{networkName}] {dexName}: API response parse error: {e}")
        transactions = []

    amountOfTransactions = len(transactions)

    logger.info(f"[{networkName}] {dexName}: {amountOfTransactions} Transactions")

    return transactions


async def getDexTransactions(
    dbConnection: Any,
    dexs: List[Dict[str, Any]]
) -> List[List[Dict[str, Any]]]:
    """Fetch transactions for multiple DEXs across different networks.

    Iterates through DEX configurations, determines the block range to fetch
    based on previously processed blocks, and makes async API calls to
    retrieve transaction data.

    Args:
        dbConnection: Active database connection for querying processed blocks.
        dexs: List of DEX configurations containing network and contract details.

    Returns:
        List of transaction lists, one per DEX that had transactions to fetch.
    """
    blockRange = getBlockRange()

    printSeparator()
    logger.info(f"Setting Up Transaction API Calls")
    printSeparator()

    # Initialize rate limiter with configured limits for API calls
    async with RateLimiter(rate_limit=API_RATE_LIMIT, concurrency_limit=API_CONCURRENCY_LIMIT) as rate_limiter:

        async with aiohttp.ClientSession() as session:

            tasks: List[asyncio.Task[List[Dict[str, Any]]]] = []
            for dex in dexs:

                # Network
                networkDetails = dex["network_details"]
                networkDbId = networkDetails["network_id"]
                networkName = networkDetails["name"].title()
                networkRpcURL = networkDetails["chain_rpc"]

                # Dex
                dexDbId = dex["dex_id"]
                dexName = dex["name"].title()

                try:

                    # Create instance of Web3
                    web3 = getWeb3Instance(
                        chainRpcURL=networkRpcURL
                    )

                    # Get the block range
                    latestBlockNumber = web3.eth.block_number

                    lastProcessedBlock = getLatestProcessedBlockNetworkIdAndDexId(
                        dbConnection=dbConnection,
                        networkDbId=networkDbId,
                        dexDbId=dexDbId
                    )

                    if lastProcessedBlock:

                        if lastProcessedBlock >= latestBlockNumber:
                            continue

                        nextBlock = lastProcessedBlock + 1
                        blocksToProcess = latestBlockNumber - nextBlock
                        if blocksToProcess > MAX_CATCHUP_BLOCKS:
                            startingBlock = latestBlockNumber - blockRange
                        else:
                            startingBlock = nextBlock

                    else:
                        startingBlock = latestBlockNumber - blockRange

                    amountOfBlocks = latestBlockNumber - startingBlock

                    logger.info(f"[{networkName}] {dexName}: {amountOfBlocks} Blocks")

                    contractsToGetTransactionsFor = ["router"]

                    for contractType in contractsToGetTransactionsFor:

                        apiEndpoint = networkDetails["explorer_api_prefix"]
                        apiToken = networkDetails["explorer_api_key"]
                        contractAddress = dex[contractType]
                        normalisedContractAddress = ''.join(e for e in contractAddress if e.isalnum())

                        apiUrl = f"{apiEndpoint}/api?module=account&action=txlist&address={normalisedContractAddress}&startblock={startingBlock}&endblock={latestBlockNumber}&sort=asc"

                        if apiToken:
                            apiUrl = f"{apiUrl}&apikey={apiToken}"

                        tasks.append(
                            asyncio.ensure_future(getTransactions(clientSession=session,
                                                                  rateLimiter=rate_limiter,
                                                                  apiUrl=apiUrl,
                                                                  networkName=networkName,
                                                                  dexName=dexName,
                                                                  )
                                                  ))

                except (ConnectionError, TimeoutError, ValueError) as e:
                    logger.warning(f"[{networkName}] [{dexName}] Failed to fetch transactions: {e}")
                    continue

            printSeparator(True)

            printSeparator()
            logger.info(f"Gathering Transactions")
            printSeparator()

            results = await asyncio.gather(*tasks)

            printSeparator(True)

            return results
