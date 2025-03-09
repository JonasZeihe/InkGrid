"""
Logging configuration for the InkGrid application.
Ensures a unified logging setup for both console and file outputs.
"""

import logging


def setup_logger(to_file=False, log_file="inkgrid.log", level=logging.INFO):
    """
    Creates and returns a logger with optional file logging.

    Args:
        to_file (bool): Whether to log to a file.
        log_file (str): Log file path if file logging is enabled.
        level (int): Logging level (e.g., logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("app_logger")
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    if to_file:
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger
