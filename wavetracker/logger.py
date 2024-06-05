import logging
from rich.logging import RichHandler


def get_logger(name: str) -> logging.Logger:
    """Get a logger with RichHandler for nice formatting."""
    format = "%(message)s"
    logging.basicConfig(
        level="INFO",
        format=format,
        datefmt="[%X]",
        handlers=[RichHandler(level="INFO")],
    )
    log = logging.getLogger(name)

    return log
