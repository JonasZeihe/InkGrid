"""
Utility functions for InkGrid. Handles reading color files and sanitizing IDs.
"""

import re


def read_color_file(file_path):
    """
    Reads colors from a file. Each line can have 'GroupName: #RRGGBB'.
    Returns a list of (group, color) tuples.
    """
    colors = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    group, color = line.split(":", 1)
                    group = group.strip()
                    color = color.strip()
                    if re.match(r"^#[0-9A-Fa-f]{6}$", color):
                        colors.append((group, color))
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    return colors


def sanitize_id(text):
    """
    Replaces non-alphanumeric characters with underscores for safe SVG usage.
    """
    return re.sub(r"\W+", "_", text)
