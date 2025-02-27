# src/inkgrid/generate.py

import os
from datetime import datetime
import svgwrite
from inkgrid.utils import sanitize_id

def generate_svg(colors, input_filename, output_file=None):
    """
    Generates an SVG file with color swatches, organized for light and dark backgrounds.

    Args:
        colors (list of tuple): List of (group, color) tuples.
        input_filename (str): Original color file name.
        output_file (str): Optional path for saving the SVG file.
    """
    swatch_width = 120
    swatch_height = 120
    margin = 40
    padding = 20
    text_height = 20
    text_padding_top = 40
    swatches_per_row = 7
    corner_radius = 10
    total_colors = len(colors)
    rows = (total_colors // swatches_per_row) + (
        1 if total_colors % swatches_per_row != 0 else 0
    )
    content_width = (
        (swatch_width + padding) * min(swatches_per_row, total_colors) - padding
    )
    content_height = (
        (swatch_height + padding + text_height * 2) * rows - padding
    )
    svg_width = content_width + 2 * margin
    svg_height = (content_height * 2) + 4 * margin + text_padding_top
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_filename))[0]
        output_file = f"{timestamp}_{base_name}.svg"
    dwg = svgwrite.Drawing(output_file, size=(svg_width, svg_height), profile="tiny")
    bg = dwg.g(id="Backgrounds")
    bg.add(
        dwg.rect(
            insert=(margin, margin + text_padding_top),
            size=(content_width + 2 * padding, content_height + 2 * padding),
            fill="white",
            rx=corner_radius,
            ry=corner_radius,
            id="LightBackground",
        )
    )
    bg.add(
        dwg.rect(
            insert=(margin, margin + text_padding_top + content_height + 2 * margin),
            size=(content_width + 2 * padding, content_height + 2 * padding),
            fill="black",
            rx=corner_radius,
            ry=corner_radius,
            id="DarkBackground",
        )
    )
    dwg.add(bg)
    light_group = dwg.g(id="LightModeSwatches")
    dark_group = dwg.g(id="DarkModeSwatches")
    for i, (group, color) in enumerate(colors):
        s_id = sanitize_id(group)
        row = i // swatches_per_row
        col = i % swatches_per_row
        x = margin + padding + col * (swatch_width + padding)
        y_top = (
            margin
            + padding
            + text_padding_top
            + row * (swatch_height + padding + text_height * 2)
        )
        y_bottom = y_top + content_height + 2 * margin
        sw_light = dwg.g(id=f"{s_id}_Light")
        sw_light.add(
            dwg.rect(
                insert=(x, y_top),
                size=(swatch_width, swatch_height),
                fill=color,
                rx=corner_radius,
                ry=corner_radius,
            )
        )
        sw_light.add(
            dwg.text(
                group,
                insert=(x + 10, y_top - 8),
                fill="black",
                font_size="16px",
                font_family="Arial",
            )
        )
        sw_light.add(
            dwg.text(
                color,
                insert=(x + 10, y_top + swatch_height + 15),
                fill="black",
                font_size="14px",
                font_family="Arial",
            )
        )
        light_group.add(sw_light)
        sw_dark = dwg.g(id=f"{s_id}_Dark")
        sw_dark.add(
            dwg.rect(
                insert=(x, y_bottom),
                size=(swatch_width, swatch_height),
                fill=color,
                rx=corner_radius,
                ry=corner_radius,
            )
        )
        sw_dark.add(
            dwg.text(
                group,
                insert=(x + 10, y_bottom - 8),
                fill="white",
                font_size="16px",
                font_family="Arial",
            )
        )
        sw_dark.add(
            dwg.text(
                color,
                insert=(x + 10, y_bottom + swatch_height + 15),
                fill="white",
                font_size="14px",
                font_family="Arial",
            )
        )
        dark_group.add(sw_dark)
    dwg.add(light_group)
    dwg.add(dark_group)
    dwg.save()
    print(f"SVG saved as {output_file}")
