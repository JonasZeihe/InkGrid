#!/usr/bin/env python3
"""
SVG generation for InkGrid.
Creates color swatch layouts for both light and dark backgrounds,
with dynamic grouping by category, optimal positioning, and a clean layer structure.
"""

import os
import re
import math
from datetime import datetime
from collections import OrderedDict
import svgwrite
from app.utils import sanitize_id

SWATCH_WIDTH = 120
SWATCH_HEIGHT = 120
MAX_SWATCHES_PER_ROW = 13
HORIZONTAL_PADDING = 20
VERTICAL_PADDING = 20
MARGIN = 40
GROUP_SPACING = 40
LABEL_FONT_SIZE = "16px"
HEX_FONT_SIZE = "14px"
LABEL_OFFSET_X = 10
HEX_OFFSET_X = 10
LABEL_OFFSET_Y = 5
HEX_OFFSET_Y = 15


def parse_colors_from_file(file_path: str) -> OrderedDict:
    """
    Parses a text file containing color palette definitions into an ordered dictionary of groups.

    The file should have lines in the format "GroupName Number [optional descriptor]: #HEXCODE".
    Blank lines separate groups, and lines starting with '#' are ignored.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        OrderedDict: Mapping of group names to lists of hex color codes.
    """
    groups = OrderedDict()
    current_group = None
    with open(file_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                if not stripped:
                    current_group = None
                continue
            parts = stripped.split(":")
            if len(parts) < 2:
                continue
            left = parts[0].strip()
            hex_color = parts[1].strip().split()[0]
            m = re.match(r"^(.+?)\s+\d+", left)
            group_name = m.group(1).strip() if m else left
            if current_group is None:
                current_group = group_name
            if current_group != group_name:
                current_group = group_name
            if current_group not in groups:
                groups[current_group] = []
            groups[current_group].append(hex_color)
    return groups


def calculate_content_dimensions(grouped_colors: OrderedDict) -> tuple:
    """
    Calculates the overall content width and height based on grouped colors.

    Args:
        grouped_colors (OrderedDict): Mapping of group names to lists of hex color codes.

    Returns:
        tuple: (content_width, content_height)
    """
    max_row_swatches = 0
    total_rows = 0
    LABEL_HEIGHT = 20
    HEX_HEIGHT = 20
    ROW_HEIGHT = LABEL_HEIGHT + SWATCH_HEIGHT + HEX_HEIGHT
    for cols in grouped_colors.values():
        group_rows = math.ceil(len(cols) / MAX_SWATCHES_PER_ROW)
        total_rows += group_rows
        for row in range(group_rows):
            start = row * MAX_SWATCHES_PER_ROW
            row_count = len(cols[start : start + MAX_SWATCHES_PER_ROW])
            if row_count > max_row_swatches:
                max_row_swatches = row_count
    content_width = (
        max_row_swatches * SWATCH_WIDTH + (max_row_swatches - 1) * HORIZONTAL_PADDING
    )
    num_groups = len(grouped_colors)
    total_inner_padding = (total_rows - num_groups) * VERTICAL_PADDING
    content_height = (
        total_rows * ROW_HEIGHT + total_inner_padding + (num_groups - 1) * GROUP_SPACING
    )
    return content_width, content_height


def create_backgrounds(
    dwg: svgwrite.Drawing, svg_width: int, bg_height: int, gap_between: int
) -> None:
    """
    Creates two background rectangles for light and dark modes with symmetric margins.

    Args:
        dwg (svgwrite.Drawing): The SVG drawing object.
        svg_width (int): Total width of the SVG.
        bg_height (int): Height of each background section.
        gap_between (int): Vertical gap between the two background sections.
    """
    backgrounds = dwg.g(id="Backgrounds")
    backgrounds.add(
        dwg.rect(
            insert=(0, 0),
            size=(svg_width, bg_height),
            fill="white",
            rx=MARGIN // 2,
            ry=MARGIN // 2,
            id="LightBackground",
        )
    )
    dark_y = bg_height + gap_between
    backgrounds.add(
        dwg.rect(
            insert=(0, dark_y),
            size=(svg_width, bg_height),
            fill="black",
            rx=MARGIN // 2,
            ry=MARGIN // 2,
            id="DarkBackground",
        )
    )
    dwg.add(backgrounds)


def create_swatch_groups(
    dwg: svgwrite.Drawing, grouped_colors: OrderedDict, bg_height: int
) -> None:
    """
    Places color swatches for both light and dark modes grouped by category.
    Each group is displayed in its own row(s).
    """
    light_group = dwg.g(id="LightModeSwatches")
    dark_group = dwg.g(id="DarkModeSwatches")
    LABEL_HEIGHT = 20
    HEX_HEIGHT = 20
    ROW_HEIGHT = LABEL_HEIGHT + SWATCH_HEIGHT + HEX_HEIGHT
    current_y = MARGIN
    for group_label, entries in grouped_colors.items():
        group_rows = math.ceil(len(entries) / MAX_SWATCHES_PER_ROW)
        for row in range(group_rows):
            start = row * MAX_SWATCHES_PER_ROW
            row_entries = entries[start : start + MAX_SWATCHES_PER_ROW]
            current_x = MARGIN
            for label, color in row_entries:
                add_swatch(
                    light_group, dwg, label, color, current_x, current_y, "black"
                )
                dark_y = current_y + bg_height + MARGIN
                add_swatch(dark_group, dwg, label, color, current_x, dark_y, "white")
                current_x += SWATCH_WIDTH + HORIZONTAL_PADDING
            current_y += ROW_HEIGHT + VERTICAL_PADDING
        current_y += GROUP_SPACING - VERTICAL_PADDING
    dwg.add(light_group)
    dwg.add(dark_group)


def add_swatch(
    group: svgwrite.container.Group,
    dwg: svgwrite.Drawing,
    label: str,
    color: str,
    x: int,
    y: int,
    text_color: str,
) -> None:
    """
    Adds a single color swatch with its label and hex code.

    Args:
        group (svgwrite.container.Group): The SVG group to add the swatch to.
        dwg (svgwrite.Drawing): The SVG drawing object.
        label (str): The category label of the color.
        color (str): The hex color code.
        x (int): The x-coordinate for the swatch.
        y (int): The y-coordinate for the top of the swatch.
        text_color (str): The text color ("black" or "white").
    """
    s_id = sanitize_id(label)
    swatch_group = dwg.g(id=f"{s_id}_{x}_{y}")
    swatch_group.add(
        dwg.rect(
            insert=(x, y), size=(SWATCH_WIDTH, SWATCH_HEIGHT), fill=color, rx=10, ry=10
        )
    )
    swatch_group.add(
        dwg.text(
            label,
            insert=(x + LABEL_OFFSET_X, y - LABEL_OFFSET_Y),
            fill=text_color,
            font_size=LABEL_FONT_SIZE,
            font_family="Arial",
        )
    )
    swatch_group.add(
        dwg.text(
            color,
            insert=(x + HEX_OFFSET_X, y + SWATCH_HEIGHT + HEX_OFFSET_Y),
            fill=text_color,
            font_size=HEX_FONT_SIZE,
            font_family="Arial",
        )
    )
    group.add(swatch_group)


def generate_svg_from_groups(
    grouped_colors, input_filename: str, output_file: str = None
) -> None:
    """
    Generates an SVG file from grouped colors.
    Args:
        grouped_colors (OrderedDict or list): Either a mapping of main groups to lists of (label, hex) pairs
          or a list of (main_group, full_label, hex) tuples.
        input_filename (str): Source filename used for naming the output.
        output_file (str, optional): Optional output file path. If not provided, a timestamped filename is generated.
    """
    if isinstance(grouped_colors, list):
        temp = OrderedDict()
        for item in grouped_colors:
            if len(item) == 3:
                group, label, color = item
            else:
                group, color = item
                label = group
            temp.setdefault(group, []).append((label, color))
        grouped_colors = temp
    content_width, content_height = calculate_content_dimensions(grouped_colors)
    svg_width = content_width + 2 * MARGIN
    gap_between = MARGIN
    bg_height = content_height + 2 * MARGIN
    svg_height = bg_height * 2 + gap_between
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_filename))[0]
        output_file = f"{timestamp}_{base_name}.svg"
    dwg = svgwrite.Drawing(output_file, size=(svg_width, svg_height), profile="tiny")
    create_backgrounds(dwg, svg_width, bg_height, gap_between)
    create_swatch_groups(dwg, grouped_colors, bg_height)
    dwg.save()
    print(f"SVG saved as {output_file}")


generate_svg = generate_svg_from_groups

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: generate.py <input_file> [output_file]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    grouped_colors = parse_colors_from_file(input_file)
    generate_svg_from_groups(grouped_colors, input_file, output_file)
