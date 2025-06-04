# src/app/export.py
"""
JSON generation for InkGrid.
Creates a JSON file for the InkGrid-Tokens Figma plugin,
to import it as color styles directly in Figma.
"""

import json
import os
from collections import defaultdict


def export_json_for_figma(colors, input_filename: str, output_dir: str):
    """
    Converts color list into plugin-compatible JSON and writes to file.

    Args:
        colors (list): List of (main_group, full_label, hex) tuples
        input_filename (str): Used to generate a matching filename
        output_dir (str): Directory where JSON will be saved
    """
    grouped = defaultdict(dict)
    for group, label, hex_code in colors:
        grouped[group][label] = hex_code

    output_data = dict(grouped)

    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    json_filename = f"{base_name}_figma_tokens.json"
    json_path = os.path.join(output_dir, json_filename)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    return json_path
