"""
Utility functions for InkGrid. Handles reading color files and sanitizing IDs.
"""

import re
import os
import logging

logger = logging.getLogger("app_logger")


def read_color_file(file_path):
    """
    Reads colors from a file. Each line can have 'GroupName: #RRGGBB'.
    Returns a list of (group, color) tuples.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return []

    colors = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                group, color = map(str.strip, line.split(":", 1))
                if re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
                    colors.append((group, color))

    if not colors:
        logger.warning(f"No valid colors found in {file_path}")

    return colors


def sanitize_id(text):
    """
    Replaces non-alphanumeric characters with underscores for safe SVG usage.
    """
    return re.sub(r"\W+", "_", text)
