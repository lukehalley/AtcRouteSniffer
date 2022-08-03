from src.chain.decode.decode_Tx import decodeTx


def decodeTransactions(dexs):

    routes = []

    for dex in dexs:

        dexRouterAddress = dex["router"]
        dexRouterABI = dex["router_abi"]
        dexTransactions = dex["transactions"]

        # Create the dict of decode tasks
        decodedTransactions = [decodeTx(address=dexRouterAddress, transaction=transaction, abi=dexRouterABI) for transaction in dexTransactions]

        # Filter out the invalid results
        finalDecodedTransactions = [decodedTransaction for decodedTransaction in decodedTransactions if isinstance(decodedTransaction, dict) and "path" in decodedTransaction["params"]]

        collectedRoutes = {}

        for finalDecodedTransaction in finalDecodedTransactions:

            routeUsed = finalDecodedTransaction["params"]["path"]
            routeName = f"{routeUsed[0]}-{routeUsed[-1]}"

            isLoopRoute = routeUsed[0] == routeUsed[-1]

            if not isLoopRoute:

                if routeName not in collectedRoutes:
                    collectedRoutes[routeName] = []

                routeObject = {
                    "method": finalDecodedTransaction["name"],
                    "route": routeUsed,
                    "blockNumber": finalDecodedTransaction["blockNumber"]
                }

                if "amountIn" in finalDecodedTransaction["params"]:
                    routeObject["amountIn"] = finalDecodedTransaction["params"]["amountIn"]

                if "amountOutMin" in finalDecodedTransaction["params"]:
                    routeObject["amountOutMin"] = finalDecodedTransaction["params"]["amountOutMin"]

                if routeObject not in collectedRoutes[routeName]:
                    collectedRoutes[routeName].append(routeObject)

                x = 1

        dex["routes"] = collectedRoutes

    return dexs