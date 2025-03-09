"""
SVG generation for InkGrid.
Creates color swatch layouts for both light and dark backgrounds.
"""

import os
from datetime import datetime
import svgwrite
from app.utils import sanitize_id


def generate_svg(colors, input_filename, output_file=None):
    """
    Generates an SVG file with color swatches.

    Args:
        colors (list[tuple]): (group, color) pairs.
        input_filename (str): Source filename for naming.
        output_file (str): Optional override for output path.
    """
    swatch_size = (120, 120)
    margin, padding, text_height, text_padding_top = 40, 20, 20, 40
    swatches_per_row, corner_radius = 7, 10
    total_colors = len(colors)

    rows = -(-total_colors // swatches_per_row)
    content_width = (swatch_size[0] + padding) * min(
        swatches_per_row, total_colors
    ) - padding
    content_height = (swatch_size[1] + padding + text_height * 2) * rows - padding
    svg_width = content_width + 2 * margin
    svg_height = (content_height * 2) + 4 * margin + text_padding_top

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_filename))[0]
        output_file = f"{timestamp}_{base_name}.svg"

    dwg = svgwrite.Drawing(output_file, size=(svg_width, svg_height), profile="tiny")
    create_backgrounds(
        dwg, content_width, content_height, margin, text_padding_top, corner_radius
    )
    create_swatch_groups(
        dwg,
        colors,
        margin,
        padding,
        swatch_size,
        text_height,
        text_padding_top,
        content_height,
    )
    dwg.save()
    print(f"SVG saved as {output_file}")


def create_backgrounds(
    dwg, content_width, content_height, margin, text_padding_top, corner_radius
):
    """
    Adds rectangles for light and dark backgrounds.
    """
    bg = dwg.g(id="Backgrounds")
    bg.add(
        dwg.rect(
            insert=(margin, margin + text_padding_top),
            size=(content_width + 40, content_height + 40),
            fill="white",
            rx=corner_radius,
            ry=corner_radius,
            id="LightBackground",
        )
    )
    bg.add(
        dwg.rect(
            insert=(margin, margin + text_padding_top + content_height + 80),
            size=(content_width + 40, content_height + 40),
            fill="black",
            rx=corner_radius,
            ry=corner_radius,
            id="DarkBackground",
        )
    )
    dwg.add(bg)


def create_swatch_groups(
    dwg,
    colors,
    margin,
    padding,
    swatch_size,
    text_height,
    text_padding_top,
    content_height,
):
    """
    Places color swatches in separate groups for light and dark modes.
    """
    light_group = dwg.g(id="LightModeSwatches")
    dark_group = dwg.g(id="DarkModeSwatches")

    for i, (group_label, color) in enumerate(colors):
        x, y_top, y_bottom = calculate_positions(
            i,
            margin,
            padding,
            swatch_size,
            text_height,
            text_padding_top,
            content_height,
        )
        add_swatch(light_group, dwg, group_label, color, x, y_top, "black")
        add_swatch(dark_group, dwg, group_label, color, x, y_bottom, "white")

    dwg.add(light_group)
    dwg.add(dark_group)


def calculate_positions(
    i, margin, padding, swatch_size, text_height, text_padding_top, content_height
):
    """
    Returns x-coord, y-coord for top block, y-coord for bottom block.
    """
    row, col = divmod(i, 7)
    x = margin + padding + col * (swatch_size[0] + padding)
    y_top = (
        margin
        + padding
        + text_padding_top
        + row * (swatch_size[1] + padding + text_height * 2)
    )
    y_bottom = y_top + content_height + 80
    return x, y_top, y_bottom


def add_swatch(group, dwg, label, color, x, y, text_color):
    """
    Creates one color swatch with label and color text.
    """
    s_id = sanitize_id(label)
    swatch = dwg.g(id=f"{s_id}")
    swatch.add(dwg.rect(insert=(x, y), size=(120, 120), fill=color, rx=10, ry=10))
    swatch.add(
        dwg.text(
            label,
            insert=(x + 10, y - 8),
            fill=text_color,
            font_size="16px",
            font_family="Arial",
        )
    )
    swatch.add(
        dwg.text(
            color,
            insert=(x + 10, y + 135),
            fill=text_color,
            font_size="14px",
            font_family="Arial",
        )
    )
    group.add(swatch)
