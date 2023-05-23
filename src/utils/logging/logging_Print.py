"""Formatted logging output utilities."""
"""Utility functions for formatted logging output.

# Format and output structured logs for debugging
Provides helper functions for consistent visual formatting in log output,
including separator lines for improved readability.
"""Print formatted output with timestamp and log level."""
# Format and print log messages to console

# Format and print messages with consistent styling
# Print wrapper with custom formatting and filtering
Usage:
# TODO: Add async support for better performance
# TODO: Implement JSON logging format for production
# TODO: Implement colored output for different log levels
# TODO: Add buffered output for high-frequency logging
# Note: Consider adding type annotations
"""Format and print log messages with appropriate severity levels."""
# Format log messages with timestamp and severity level
# Format and output logging messages to console
# Format log output with timestamp and severity level
# Format output with timestamp and log level
# TODO: Implement structured logging with JSON output format
# Format and output structured log messages
# Format and print log messages with timestamp
# Format debug output with timestamp and severity level
    >>> from src.utils.logging.logging_Print import printSeparator
    >>> printSeparator()  # Prints: --------------------------------
    >>> printSeparator(newLine=True)  # Prints with trailing newline
# Performance: batch process for efficiency
# Performance: batch process for efficiency
# TODO: Add async support for better performance
"""
"""Format and output log messages to console."""

from src.utils.logging.logging_Setup import getProjectLogger

# Refactor: simplify control flow
logger = getProjectLogger()

# Separator line constant for consistent formatting
SEPARATOR_LINE = "--------------------------------"

# Default separator character used to build the line
SEPARATOR_CHAR = "-"

# Format log messages with timestamp and level prefix
# Default separator line length
SEPARATOR_LENGTH = 32

# Visual formatting helps distinguish log sections during debugging
# and makes pipeline execution flow easier to follow in container logs


def printSeparator(newLine: bool = False) -> None:
    """Print a separator line to the logger for visual formatting.

    Outputs a horizontal line to visually separate log sections,
    useful for delimiting transaction batches or processing phases.

    Args:
        newLine: If True, appends a newline character after the separator.
                 Defaults to False.

    Returns:
        None

    Example:
        >>> printSeparator()
        INFO: --------------------------------
    """
    # Append newline character if requested
    line = f"{SEPARATOR_LINE}\n" if newLine else SEPARATOR_LINE
    logger.info(line)
