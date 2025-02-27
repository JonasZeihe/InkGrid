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
    margin = 20
    text_height = 24
    swatches_per_row = 5
    corner_radius = 10

    total_colors = len(colors)
    rows = (total_colors // swatches_per_row) + (1 if total_colors % swatches_per_row != 0 else 0)
    content_width = (swatch_width + margin) * min(swatches_per_row, total_colors) - margin
    content_height = (swatch_height + margin + text_height * 2) * rows - margin

    svg_width = content_width + 2 * margin
    svg_height = (content_height * 2) + 3 * margin

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_filename))[0]
        output_file = f"{timestamp}_{base_name}.svg"

    dwg = svgwrite.Drawing(output_file, size=(svg_width, svg_height), profile='tiny')

    # Backgrounds for Light and Dark sections
    dwg.add(dwg.rect(insert=(margin / 2, margin / 2), size=(svg_width - margin, svg_height / 2 - margin), fill="white", rx=corner_radius, ry=corner_radius))
    dwg.add(dwg.rect(insert=(margin / 2, svg_height / 2 + margin / 2), size=(svg_width - margin, svg_height / 2 - margin), fill="black", rx=corner_radius, ry=corner_radius))

    # Swatches and Text in both Light and Dark sections
    for index, (group, color) in enumerate(colors):
        sanitized_id = sanitize_id(group)
        row = index // swatches_per_row
        col = index % swatches_per_row
        x = margin + col * (swatch_width + margin)
        y_top = margin + row * (swatch_height + margin + text_height * 2)
        y_bottom = y_top + svg_height / 2

        # Light mode (top) - dark text on light background
        swatch_group_light = dwg.g(id=f"{sanitized_id}_Top_Swatch")
        swatch_group_light.add(dwg.rect(insert=(x, y_top), size=(swatch_width, swatch_height), fill=color, rx=corner_radius, ry=corner_radius))
        swatch_group_light.add(dwg.text(group, insert=(x + 10, y_top - 10), fill='black', font_size='15px', font_family='Arial'))
        swatch_group_light.add(dwg.text(color, insert=(x + 10, y_top + swatch_height + 18), fill='black', font_size='12px', font_family='Arial'))
        dwg.add(swatch_group_light)

        # Dark mode (bottom) - light text on dark background
        swatch_group_dark = dwg.g(id=f"{sanitized_id}_Bottom_Swatch")
        swatch_group_dark.add(dwg.rect(insert=(x, y_bottom), size=(swatch_width, swatch_height), fill=color, rx=corner_radius, ry=corner_radius))
        swatch_group_dark.add(dwg.text(group, insert=(x + 10, y_bottom - 10), fill='white', font_size='15px', font_family='Arial'))
        swatch_group_dark.add(dwg.text(color, insert=(x + 10, y_bottom + swatch_height + 18), fill='white', font_size='12px', font_family='Arial'))
        dwg.add(swatch_group_dark)

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
