# src/inkgrid/utils.py

import re

def read_color_file(file_path):
    """
    Reads colors from a file. Each line should contain a color in hex format,
    with an optional group name separated by a colon.

    Args:
        file_path (str): Path to the input color file.

    Returns:
        list of tuple: List of (group, color) tuples.
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
        return colors
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []

def sanitize_id(text):
    """
    Sanitizes a text to make it suitable for use as an ID.

    Args:
        text (str): The text to sanitize.

    Returns:
        str: Sanitized text.
    """
    return re.sub(r"\W+", "_", text)
