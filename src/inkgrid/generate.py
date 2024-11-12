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
    swatch_width, swatch_height, margin, text_height, corner_radius = 120, 120, 20, 24, 10
    swatches_per_row = 5
    total_colors = len(colors)
    rows = (total_colors // swatches_per_row) + (1 if total_colors % swatches_per_row != 0 else 0)
    content_width = (swatch_width + margin) * min(swatches_per_row, total_colors) - margin
    content_height = (swatch_height + margin + text_height * 2) * rows - margin

    svg_width, svg_height = content_width + 2 * margin, (content_height * 2) + 3 * margin

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_filename))[0]
        output_file = f"{timestamp}_{base_name}.svg"

    dwg = svgwrite.Drawing(output_file, size=(svg_width, svg_height), profile='tiny')

    # Backgrounds for Light and Dark sections
    dwg.add(dwg.rect(insert=(margin / 2, margin / 2), size=(svg_width - margin, svg_height / 2 - margin), fill="white", rx=corner_radius, ry=corner_radius))
    dwg.add(dwg.rect(insert=(margin / 2, svg_height / 2 + margin / 2), size=(svg_width - margin, svg_height / 2 - margin), fill="black", rx=corner_radius, ry=corner_radius))

    for index, (group, color) in enumerate(colors):
        sanitized_id = sanitize_id(group)
        row, col = index // swatches_per_row, index % swatches_per_row
        x, y_top = margin + col * (swatch_width + margin), margin + row * (swatch_height + margin + text_height * 2)
        y_bottom = y_top + svg_height / 2

        # Light mode (top) - dark text on light background
        dwg.add(dwg.rect(insert=(x, y_top), size=(swatch_width, swatch_height), fill=color, rx=corner_radius, ry=corner_radius))
        dwg.add(dwg.text(group, insert=(x + 10, y_top - 10), fill='black', font_size='15px', font_family='Arial'))
        dwg.add(dwg.text(color, insert=(x + 10, y_top + swatch_height + 18), fill='black', font_size='12px', font_family='Arial'))

        # Dark mode (bottom) - light text on dark background
        dwg.add(dwg.rect(insert=(x, y_bottom), size=(swatch_width, swatch_height), fill=color, rx=corner_radius, ry=corner_radius))
        dwg.add(dwg.text(group, insert=(x + 10, y_bottom - 10), fill='white', font_size='15px', font_family='Arial'))
        dwg.add(dwg.text(color, insert=(x + 10, y_bottom + swatch_height + 18), fill='white', font_size='12px', font_family='Arial'))

    dwg.save()
    print(f"SVG saved as {output_file}")
