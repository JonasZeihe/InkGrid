import svgwrite
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os
import re


def read_color_file(file_path):
    colors = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                group, color = line.split(":", 1)
                group = group.strip()
                color = color.strip()
                if color.startswith("#"):
                    colors.append((group, color))
    return colors


def sanitize_id(text):
    return re.sub(r'\W+', '_', text)


def generate_svg(colors, input_filename, output_file=None):
    swatch_width, swatch_height = 120, 120
    margin = 40
    padding = 20
    text_height = 20
    text_padding_top = 40
    swatches_per_row = 7
    corner_radius = 10

    total_colors = len(colors)
    rows = (total_colors // swatches_per_row) + (1 if total_colors % swatches_per_row != 0 else 0)
    content_width = (swatch_width + padding) * min(swatches_per_row, total_colors) - padding
    content_height = (swatch_height + padding + text_height * 2) * rows - padding

    svg_width = content_width + 2 * margin
    svg_height = (content_height * 2) + 4 * margin + text_padding_top

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_filename))[0]
        output_file = f"{timestamp}_{base_name}.svg"

    dwg = svgwrite.Drawing(output_file, size=(svg_width, svg_height), profile='tiny')

    backgrounds_group = dwg.g(id="Backgrounds")
    backgrounds_group.add(dwg.rect(insert=(margin, margin + text_padding_top), size=(content_width + 2 * padding, content_height + 2 * padding),
                                   fill="white", rx=corner_radius, ry=corner_radius, id="LightBackground"))
    backgrounds_group.add(dwg.rect(insert=(margin, margin + text_padding_top + content_height + 2 * margin),
                                   size=(content_width + 2 * padding, content_height + 2 * padding),
                                   fill="black", rx=corner_radius, ry=corner_radius, id="DarkBackground"))
    dwg.add(backgrounds_group)

    swatches_group_light = dwg.g(id="LightModeSwatches")
    swatches_group_dark = dwg.g(id="DarkModeSwatches")

    for index, (group, color) in enumerate(colors):
        sanitized_id = sanitize_id(group)
        row = index // swatches_per_row
        col = index % swatches_per_row
        x = margin + padding + col * (swatch_width + padding)
        y_top = margin + padding + text_padding_top + row * (swatch_height + padding + text_height * 2)
        y_bottom = y_top + content_height + 2 * margin

        swatch_light = dwg.g(id=f"{sanitized_id}_Light")
        swatch_light.add(dwg.rect(insert=(x, y_top), size=(swatch_width, swatch_height), fill=color, rx=corner_radius, ry=corner_radius))
        swatch_light.add(dwg.text(group, insert=(x + 10, y_top - 8), fill='black', font_size='16px', font_family='Arial'))
        swatch_light.add(dwg.text(color, insert=(x + 10, y_top + swatch_height + 15), fill='black', font_size='14px', font_family='Arial'))
        swatches_group_light.add(swatch_light)

        swatch_dark = dwg.g(id=f"{sanitized_id}_Dark")
        swatch_dark.add(dwg.rect(insert=(x, y_bottom), size=(swatch_width, swatch_height), fill=color, rx=corner_radius, ry=corner_radius))
        swatch_dark.add(dwg.text(group, insert=(x + 10, y_bottom - 8), fill='white', font_size='16px', font_family='Arial'))
        swatch_dark.add(dwg.text(color, insert=(x + 10, y_bottom + swatch_height + 15), fill='white', font_size='14px', font_family='Arial'))
        swatches_group_dark.add(swatch_dark)

    dwg.add(swatches_group_light)
    dwg.add(swatches_group_dark)
    dwg.save()
    print(f"SVG saved as {output_file}")


def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select color file", filetypes=(("Text Files", "*.txt"),))

    if file_path:
        colors = read_color_file(file_path)
        if colors:
            generate_svg(colors, input_filename=file_path)
        else:
            print("No valid colors found in the file.")
    else:
        print("No file selected")


if __name__ == "__main__":
    main()
