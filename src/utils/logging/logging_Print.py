"""Utility functions for formatted logging output.

Provides helper functions for consistent visual formatting in log output,
including separator lines for improved readability.
"""

from src.utils.logging.logging_Setup import getProjectLogger

logger = getProjectLogger()

# Separator line constant for consistent formatting
SEPARATOR_LINE = "--------------------------------"


def printSeparator(newLine: bool = False) -> None:
    """Print a separator line to the logger for visual formatting.

    Args:
        newLine: If True, appends a newline character after the separator.
                 Defaults to False.

    Returns:
        None
    """
    line = f"{SEPARATOR_LINE}\n" if newLine else SEPARATOR_LINE
    logger.info(line)
