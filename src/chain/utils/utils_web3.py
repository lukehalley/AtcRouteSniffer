from web3 import Web3
from web3.middleware import geth_poa_middleware

def getWeb3Instance(rpcUrl):
    web3 = Web3(Web3.HTTPProvider(rpcUrl))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3