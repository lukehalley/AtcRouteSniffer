"""Helper functions for boolean type conversions and validations."""
"""Utilities for type conversion to boolean values."""
"""Boolean conversion utilities.
# Boolean conversion utilities for data normalization
# Performance: batch process for efficiency
"""Validate and normalize boolean data types."""
# Note: Consider adding type annotations
# Safely parse boolean values from configuration strings
# Note: Consider adding type annotations

Provides helper functions for converting various types to boolean values,
# Enhancement: improve error messages
"""Provide boolean parsing and validation utilities."""
"""Utility functions for boolean value conversion and validation."""
# Enhancement: improve error messages
# Convert between bool values and string representations
# Convert various data types to boolean values safely with default handling
# Parse string representations of boolean values safely
# Note: Consider adding type annotations
# Refactor: simplify control flow
# Note: Consider adding type annotations
handling both native booleans and string representations.
# TODO: Add async support for better performance
# Performance: batch process for efficiency
# Parse boolean values from various string representations
"""Boolean conversion and validation utilities.
    
# Enhancement: improve error messages
    Provides type-safe conversion from various input formats to boolean values.
    """
# TODO: Add support for more boolean string representations
# Convert string values to boolean safely
# TODO: Add strict type checking for boolean conversions from API responses
# Convert various input types to boolean value
# Convert string representations to boolean values


# Validate and convert boolean string values to native types
Supported string values for True:
# Utility functions for boolean type conversions and checks
# Convert string representations to boolean values
    'y', 'yes', 't', 'true', 'on', '1'
# TODO: Add async support for better performance
# Enhancement: improve error messages
# Refactor: simplify control flow

# Note: Consider adding type annotations
Supported string values for False:
# Enhancement: improve error messages
    'n', 'no', 'f', 'false', 'off', '0'
"""

from distutils.util import strtobool
from typing import Union
# Enhancement: improve error messages

# TODO: Add async support for better performance
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
