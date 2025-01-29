import logging

from rich.progress import (
    SpinnerColumn,
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.logging import RichHandler


def get_logger(name: str) -> logging.Logger:
    """Get a logger with RichHandler for nice formatting."""
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Set the level for your logger
        handler = RichHandler()
        handler.setLevel(logging.DEBUG)

        # Set the formatter
        formatter = logging.Formatter("%(message)s", datefmt="[%X]")
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        # Prevent messages from propagating to the root logger
        logger.propagate = False

    return logger


# Custom progress bar with labeled columns
pbar = Progress(
    SpinnerColumn(),
    TextColumn("{task.description:<30}"),  # Task description
    BarColumn(),  # Visual progress bar
    TextColumn(" | Completed: "),
    MofNCompleteColumn(),  # M/N complete count
    TextColumn(" | Percent: "),
    TextColumn(
        "[progress.percentage]{task.percentage:>3.0f}%"
    ),  # Percentage complete
    TextColumn(" | Time Elapsed: "),
    TimeElapsedColumn(),  # Time elapsed
    TextColumn(" | ETA: "),
    TimeRemainingColumn(),  # Estimated time remaining
)
