import logging

from rich.logging import RichHandler


def get_logger(name: str) -> logging.Logger:
    """Get a logger with RichHandler for nice formatting."""
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)  # Set the level for your logger
        handler = RichHandler()
        handler.setLevel(logging.INFO)

        # Set the formatter
        formatter = logging.Formatter("%(message)s", datefmt="[%X]")
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        # Prevent messages from propagating to the root logger
        logger.propagate = False

    return logger
