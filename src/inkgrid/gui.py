# src/inkgrid/gui.py

import tkinter as tk
from tkinter import filedialog

def select_color_file():
    """
    Opens a file dialog to select a color file.

    Returns:
        str: Path to the selected color file.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select color file", filetypes=(("Text Files", "*.txt"),))
    return file_path if file_path else None
