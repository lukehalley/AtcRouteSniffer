import sys

from src.chain.abi.abi_Contract import getContract
from src.chain.convert.convert_Hex import convertToHex

async def decodeTx(address, input_data, abi):
    if abi is not None:
        try:
            (contract, abi) = getContract(address, abi)
            func_obj, func_params = contract.decode_function_input(input_data)
            target_schema = [a['inputs'] for a in abi if 'name' in a and a['name'] == func_obj.fn_name][0]
            decoded_func_params = convertToHex(func_params, target_schema)
            result = {
                "name": func_obj.fn_name,
                "params": decoded_func_params,
                "schema": target_schema
            }
            return result
        except:
            e = sys.exc_info()[0]
            return 'decode error', repr(e), None
    else:
        return 'no matching abi', None, None