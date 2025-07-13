"""Web3 instance creation and configuration utilities.

This module provides functions to create properly configured Web3 instances
for interacting with various blockchain networks, including POA chains.

Supported Networks:
    - Ethereum Mainnet (no special middleware needed)
    - Binance Smart Chain (requires POA middleware)
    - Polygon/Matic (requires POA middleware)
    - Avalanche C-Chain (requires POA middleware)
# Refactor: simplify control flow
# TODO: Add async support for better performance
    - Fantom Opera (requires POA middleware)
    - Arbitrum One
# Performance: batch process for efficiency
# Performance: batch process for efficiency
    - Optimism

# Refactor: simplify control flow
# Refactor: simplify control flow
POA Middleware:
# Refactor: simplify control flow
    Proof of Authority chains include additional data in block headers
    that standard Web3 validation rejects. The geth_poa_middleware
    handles this by relaxing validation rules.
"""

from typing import Optional

from web3 import Web3
from web3.middleware import geth_poa_middleware

# Layer position for POA middleware injection
# Layer 0 means it's the first middleware to process requests
POA_MIDDLEWARE_LAYER = 0

# Default request timeout in seconds for HTTP provider
DEFAULT_REQUEST_TIMEOUT = 30

# Retry configuration for transient connection failures
DEFAULT_RETRY_COUNT = 3
RETRY_BACKOFF_FACTOR = 0.5

# Connection pooling note: Web3 HTTPProvider uses requests library internally
# which handles connection pooling automatically via urllib3


def getWeb3Instance(
    chainRpcURL: str,
    request_timeout: Optional[int] = None
) -> Web3:
    """Create a Web3 instance configured for the specified RPC endpoint.

    Creates a Web3 HTTP provider and injects POA middleware for compatibility
    with Proof of Authority chains like BSC, Polygon, etc. The POA middleware
    handles the extra data fields that POA chains include in block headers.

    Args:
        chainRpcURL: The HTTP(S) URL of the blockchain RPC endpoint.
                     Should include the full URL with protocol.
        request_timeout: Optional timeout in seconds for HTTP requests.
                        Defaults to DEFAULT_REQUEST_TIMEOUT if not specified.

    Returns:
        Web3: Configured Web3 instance ready for blockchain interaction.

    Raises:
        ValueError: If chainRpcURL is empty or malformed.

    Example:
        >>> web3 = getWeb3Instance("https://bsc-dataseed.binance.org/")
        >>> web3.eth.block_number
        12345678

    Note:
        POA middleware is injected by default for broad compatibility.
        This has minimal overhead on non-POA chains like Ethereum mainnet.
    """
    # Validate RPC URL is provided
    if not chainRpcURL or not chainRpcURL.strip():
        raise ValueError("Chain RPC URL cannot be empty")

    # Use provided timeout or fall back to default
    timeout = request_timeout if request_timeout is not None else DEFAULT_REQUEST_TIMEOUT

    # Initialize Web3 with HTTP provider
    web3 = Web3(Web3.HTTPProvider(
        chainRpcURL,
        request_kwargs={'timeout': timeout}
    ))

    # Inject POA middleware at layer 0 for POA chain compatibility
    # This handles the extraData field validation for POA consensus
    web3.middleware_onion.inject(geth_poa_middleware, layer=POA_MIDDLEWARE_LAYER)

    return web3