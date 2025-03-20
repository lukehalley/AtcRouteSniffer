"""Web3 instance creation and configuration utilities.

This module provides functions to create properly configured Web3 instances
for interacting with various blockchain networks, including POA chains.
"""

from web3 import Web3
from web3.middleware import geth_poa_middleware


def getWeb3Instance(chainRpcURL: str) -> Web3:
    """Create a Web3 instance configured for the specified RPC endpoint.

    Creates a Web3 HTTP provider and injects POA middleware for compatibility
    with Proof of Authority chains like BSC, Polygon, etc.

    Args:
        chainRpcURL: The HTTP(S) URL of the blockchain RPC endpoint.

    Returns:
        Web3: Configured Web3 instance ready for blockchain interaction.

    Example:
        >>> web3 = getWeb3Instance("https://bsc-dataseed.binance.org/")
        >>> web3.eth.block_number
        12345678
    """
    web3 = Web3(Web3.HTTPProvider(chainRpcURL))
    # Inject POA middleware for compatibility with POA chains
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3