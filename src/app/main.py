"""
Main entry point for InkGrid. Parses arguments, sets up logging,
then starts the GUI where the user can choose input and output paths.
"""

import argparse
import sys
from app.logger_config import setup_logger
from app.gui import run_app


def main():
    args = _parse_args(sys.argv[1:])
    log_file = None
    if args.logging:
        log_file = "inkgrid.log"

    logger = setup_logger(to_file=bool(args.logging), log_file=log_file)
    logger.info("InkGrid started.")
    run_app(logging_enabled=bool(args.logging))
    logger.info("InkGrid finished.")


def _parse_args(cli_args):
    parser = argparse.ArgumentParser(description="InkGrid SVG Generator")
    parser.add_argument(
        "--logging",
        action="store_true",
        help="Enable file logging alongside console output.",
    )
    return parser.parse_args(cli_args)


if __name__ == "__main__":
    main()
