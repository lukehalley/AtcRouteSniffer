"""Boolean conversion utilities.

Provides helper functions for converting various types to boolean values,
handling both native booleans and string representations.
"""

from distutils.util import strtobool
from typing import Union


def strToBool(value: Union[str, bool]) -> bool:
    """Convert a string or boolean value to a boolean type.

    Handles both native boolean values (returned as-is) and string
    representations like 'true', 'false', 'yes', 'no', '1', '0'.

    Args:
        value: The value to convert, either a bool or string representation.

    Returns:
        bool: The boolean interpretation of the input value.

    Raises:
        ValueError: If the string cannot be converted to a boolean.
    """
    if isinstance(value, bool):
        return value
    return bool(strtobool(value))
