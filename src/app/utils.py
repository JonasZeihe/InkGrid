"""
Utility functions for InkGrid. Handles reading color files and sanitizing IDs.
"""

import re
import os
import logging

logger = logging.getLogger("app_logger")


def read_color_file(file_path):
    """
    Reads colors from a file. Each line should have the format:
    'GroupName Number [optional descriptor]: #RRGGBB'.
    Returns a list of tuples: (main_group, full_label, color).
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return []

    colors = []
    import re

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                full_label, color = map(str.strip, line.split(":", 1))
                m = re.match(r"^(.+?)\s+\d+", full_label)
                main_group = m.group(1).strip() if m else full_label
                if re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
                    colors.append((main_group, full_label, color))
    if not colors:
        logger.warning(f"No valid colors found in {file_path}")
    return colors


def sanitize_id(text):
    """
    Replaces non-alphanumeric characters with underscores for safe SVG usage.
    """
    import re

    return re.sub(r"\W+", "_", text).strip("_")
