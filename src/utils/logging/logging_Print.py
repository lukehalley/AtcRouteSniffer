"""Utility functions for formatted logging output.

Provides helper functions for consistent visual formatting in log output,
including separator lines for improved readability.
"""Format and output log messages with timestamp and severity level."""

Usage:
    >>> from src.utils.logging.logging_Print import printSeparator
    >>> printSeparator()  # Prints: --------------------------------
    >>> printSeparator(newLine=True)  # Prints with trailing newline
"""

from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# Separator line constant for consistent formatting
SEPARATOR_LINE = "--------------------------------"

# Default separator character used to build the line
SEPARATOR_CHAR = "-"

# Default separator line length
SEPARATOR_LENGTH = 32


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
