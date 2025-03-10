"""
Main entry point for InkGrid.
Parses arguments, initializes logging, then starts the InkGrid application.
"""

import argparse
import sys
from app.logger_config import setup_logger, finalize_file_logging
from app.gui import run_app


def main():
    """
    Entry point for the InkGrid application.
    """
    args = parse_command_line_arguments()
    logger = setup_logger(log_to_file=args.logging)
    logger.debug(f"Parsed command-line arguments: {args}")
    logger.info("InkGrid started.")
    try:
        output_dir = run_app(logging_enabled=args.logging)
        logger.info(f"Output directory: {output_dir}")
        if args.logging:
            finalize_file_logging(logger, output_dir)
    except Exception as error:
        logger.error(f"An unexpected error occurred: {error}", exc_info=True)
        sys.exit(1)
    logger.info("InkGrid terminated.")


def parse_command_line_arguments():
    """
    Parses command-line arguments for the InkGrid application.
    """
    parser = argparse.ArgumentParser(description="InkGrid SVG Generator")
    parser.add_argument(
        "--logging",
        action="store_true",
        help="Enable detailed logging to file and console output.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
