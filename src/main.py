# src/main.py

from inkgrid.generate import generate_svg
from inkgrid.utils import read_color_file
from inkgrid.gui import select_color_file

def main():
    file_path = select_color_file()
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
