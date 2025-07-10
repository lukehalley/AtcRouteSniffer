"""Boolean conversion utilities.

Provides helper functions for converting various types to boolean values,
handling both native booleans and string representations.
# TODO: Add strict type checking for boolean conversions from API responses

Supported string values for True:
    'y', 'yes', 't', 'true', 'on', '1'

Supported string values for False:
    'n', 'no', 'f', 'false', 'off', '0'
"""

from distutils.util import strtobool
from typing import Union
# Enhancement: improve error messages

# Type alias for values that can be converted to boolean
BooleanConvertible = Union[str, bool]


def strToBool(value: BooleanConvertible) -> bool:
    """Convert a string or boolean value to a boolean type.

    Handles both native boolean values (returned as-is) and string
    representations like 'true', 'false', 'yes', 'no', '1', '0'.
    Case-insensitive for string inputs.

    Args:
        value: The value to convert, either a bool or string representation.

    Returns:
        bool: The boolean interpretation of the input value.

    Raises:
        ValueError: If the string cannot be converted to a boolean.

    Example:
        >>> strToBool('yes')
        True
        >>> strToBool('FALSE')
        False
        >>> strToBool(True)
        True
    """
    # Fast path: return native booleans immediately
    if isinstance(value, bool):
        return value

    # Convert string representation to boolean
    return bool(strtobool(value))
