"""
InkGrid Logger Component

Provides structured logging to both console and file outputs.
Automatically handles timestamped log file creation when needed.
"""

import logging
import os
import time
from logging.handlers import MemoryHandler


class Logger:
    """
    Central logging class for InkGrid. Maintains console and optional file-based logging
    with a unified formatter for consistent output.
    """

    def __init__(self, to_file=False, log_directory="logs", logger_name="InkGrid"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        self._add_console_handler()
        if to_file:
            self._add_memory_handler()

    def _add_console_handler(self):
        handler = logging.StreamHandler()
        handler.setFormatter(self._create_formatter())
        self.logger.addHandler(handler)

    def _add_memory_handler(self):
        mem_handler = MemoryHandler(capacity=10000, flushLevel=logging.CRITICAL)
        mem_handler.setFormatter(self._create_formatter())
        self.logger.addHandler(mem_handler)

    @staticmethod
    def _create_formatter():
        return logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s [File: %(filename)s, Line: %(lineno)d]"
        )

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def debug(self, message):
        self.logger.debug(message)

    @staticmethod
    def setup(log_to_file=False, log_directory="logs"):
        """
        Convenience method to create and return a Logger instance.

        Args:
            log_to_file (bool): Whether file logging should be enabled.
            log_directory (str): (Ignored here) Initial log directory if file logging is enabled.

        Returns:
            Logger: An instance of Logger.
        """
        return Logger(to_file=log_to_file, log_directory=log_directory)


def finalize_file_logging(logger_instance, output_dir, log_filename=None):
    """
    Attaches a FileHandler to the logger so that logs are written to a file in the output directory.
    Flushes any buffered logs from the MemoryHandler to the new FileHandler.

    Args:
        logger_instance (Logger): Instance of Logger (the custom class).
        output_dir (str): Output directory where the log file will be created.
        log_filename (str): Optional log file name. If not provided, a timestamped name is generated.
    """
    logger = logger_instance.logger
    if not log_filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_filename = f"inkgrid_log_{timestamp}.log"
    file_path = os.path.join(output_dir, log_filename)
    os.makedirs(output_dir, exist_ok=True)
    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logger.handlers[0].formatter)

    mem_handler = None
    for handler in logger.handlers:
        if isinstance(handler, MemoryHandler):
            mem_handler = handler
            break
    if mem_handler:
        mem_handler.setTarget(file_handler)
        mem_handler.flush()
        logger.removeHandler(mem_handler)
    logger.addHandler(file_handler)
    logger.info(f"Log file successfully created: {file_path}")


setup_logger = Logger.setup
