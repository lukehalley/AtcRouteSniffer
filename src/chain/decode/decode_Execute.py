from src.chain.decode.decode_Tx import decodeTx
from src.utils.tasks.task_AyySync import gatherWithConcurrency

async def decodeTransactions(blockInputs, routeAddress, routeAbiStr):

    # Create the dict of decode tasks
    tasks = [decodeTx(routeAddress, uniqueBlockInput, routeAbiStr) for uniqueBlockInput in blockInputs]

    # Decode all the block transactions
    results = await gatherWithConcurrency(*tasks)

    # Filter out the invalid results
    results = [result for result in results if isinstance(result, dict) and "path" in result["params"]]

    collectedRoutes = {}
    for result in results:

        routeUsed = result["params"]["path"]
        routeName = f"{routeUsed[0]}-{routeUsed[-1]}"
    
        isLoopRoute = routeUsed[0] == routeUsed[-1]
    
        if not isLoopRoute:
    
            if routeName not in collectedRoutes:
                collectedRoutes[routeName] = []
    
            routeObject = {
                "method": result["name"],
                "route": routeUsed
            }
    
            if "amountIn" in result["params"]:
                routeObject["amountIn"] = result["params"]["amountIn"]
    
            if "amountOutMin" in result["params"]:
                routeObject["amountOutMin"] = result["params"]["amountOutMin"]
    
            if routeObject not in collectedRoutes[routeName]:
                collectedRoutes[routeName].append(routeObject)

    return collectedRoutes