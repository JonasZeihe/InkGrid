"""
GUI for InkGrid. Lets the user pick multiple color files and an output folder,
generates SVGs, and (if logging is enabled) logs events via the shared logger.
"""

import os
import sys
import platform
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from app.generate import generate_svg
from app.utils import read_color_file
from app.logger_config import setup_logger


def run_app(logging_enabled=False):
    """
    Starts the InkGrid GUI and allows the user to select files and an output directory.
    Returns the selected output directory.
    """
    # Do not change the working directory globally; resources are resolved via sys._MEIPASS.
    root = tk.Tk()
    root.title("InkGrid - SVG Generator")
    root.geometry("720x520")
    root.resizable(False, False)
    root.configure(bg=_get_bg_color())

    logger = setup_logger(log_to_file=logging_enabled)
    logger.info("InkGrid GUI started.")

    bg_image = _get_background_image()
    if bg_image:
        canvas = tk.Canvas(root, width=720, height=520, highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")

    _apply_theme(root)

    frame = ttk.Frame(root, padding=15, style="Card.TFrame")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="InkGrid - SVG Generator", font=_get_font(bold=True)).pack(
        pady=10
    )

    selected_files_var = tk.StringVar(value="No files selected")
    output_folder_var = tk.StringVar(value="No folder selected")

    _create_file_selection(frame, selected_files_var)
    _create_folder_selection(frame, output_folder_var)

    ttk.Button(
        frame,
        text="Generate SVGs",
        command=lambda: _generate(
            root, selected_files_var, output_folder_var, logging_enabled, logger
        ),
        style="Primary.TButton",
    ).pack(pady=15)

    root.mainloop()

    output_dir = output_folder_var.get()
    if output_dir == "No folder selected":
        output_dir = os.getcwd()

    return output_dir


def _create_file_selection(frame, selected_files_var):
    file_frame = ttk.LabelFrame(
        frame, text="Color Files", padding=10, style="Frame.TLabelframe"
    )
    file_frame.pack(fill="x", padx=10, pady=5)
    file_label = ttk.Label(
        file_frame,
        textvariable=selected_files_var,
        wraplength=400,
        style="Label.TLabel",
    )
    file_label.pack(side="left", padx=10)
    ttk.Button(
        file_frame,
        text="Browse",
        command=lambda: _select_files(selected_files_var),
        style="Secondary.TButton",
    ).pack(side="right", padx=10)


def _create_folder_selection(frame, output_folder_var):
    folder_frame = ttk.LabelFrame(
        frame, text="Output Folder", padding=10, style="Frame.TLabelframe"
    )
    folder_frame.pack(fill="x", padx=10, pady=5)
    folder_label = ttk.Label(
        folder_frame, textvariable=output_folder_var, style="Label.TLabel"
    )
    folder_label.pack(side="left", padx=10)
    ttk.Button(
        folder_frame,
        text="Choose",
        command=lambda: _select_folder(output_folder_var),
        style="Secondary.TButton",
    ).pack(side="right", padx=10)


def _generate(root, file_var, folder_var, logging_enabled, logger):
    paths = file_var.get().split(";")
    out_dir = folder_var.get()

    if "No files selected" in paths:
        logger.warning("No color files selected.")
        messagebox.showwarning("Warning", "No color files selected.")
        return

    if out_dir == "No folder selected":
        out_dir = _get_default_output_dir()

    os.makedirs(out_dir, exist_ok=True)
    logger.info(f"Output directory set: {out_dir}")

    for path in paths:
        path = path.strip()
        if not os.path.exists(path):
            logger.error(f"File not found: {path}")
            continue

        logger.info(f"Processing file: {path}")
        colors = read_color_file(path)

        if not colors:
            logger.error(f"No valid colors found in {path}.")
            messagebox.showerror("Error", f"No valid colors found in {path}.")
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(path))[0]
        svg_name = f"{timestamp}_{base_name}.svg"
        svg_path = os.path.join(out_dir, svg_name)

        logger.info(f"Generating SVG: {svg_path}")
        generate_svg(colors, path, output_file=svg_path)
        logger.info(f"SVG saved: {svg_path}")

    logger.info("All SVGs generated successfully.")
    messagebox.showinfo("Success", f"SVGs generated at:\n{out_dir}")
    root.destroy()


def _select_files(selected_files_var):
    paths = filedialog.askopenfilenames(
        title="Select color files",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        initialdir=_get_default_directory(),
    )
    if paths:
        selected_files_var.set(";".join(paths))


def _select_folder(folder_var):
    path = filedialog.askdirectory(title="Select output folder")
    if path:
        folder_var.set(path)


def _apply_theme(root):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Card.TFrame", background="#1e1e1e", relief="raised", padding=20)
    style.configure(
        "Frame.TLabelframe", background="#1e1e1e", foreground="white", font=_get_font()
    )
    style.configure(
        "Label.TLabel", background="#1e1e1e", foreground="white", font=_get_font()
    )
    style.configure(
        "Primary.TButton", background="#0078D7", foreground="white", font=_get_font()
    )
    style.configure(
        "Secondary.TButton", background="#3A3A3A", foreground="white", font=_get_font()
    )
    style.map("Primary.TButton", background=[("active", "#005A9E")])
    style.map("Secondary.TButton", background=[("active", "#555")])


def _get_background_image():
    image_path = _resolve_image_path("background.png")
    if not image_path:
        return None
    img = Image.open(image_path).convert("RGBA")
    img = img.resize((720, 520), Image.Resampling.LANCZOS)
    img = _adjust_opacity(img, 0.2)
    return ImageTk.PhotoImage(img)


def _resolve_image_path(filename):
    base_dir = (
        os.path.join(sys._MEIPASS, "images")
        if getattr(sys, "frozen", False)
        else os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "images")
        )
    )
    potential_path = os.path.join(base_dir, filename)
    return potential_path if os.path.exists(potential_path) else None


def _adjust_opacity(img, alpha):
    overlay = Image.new("RGBA", img.size, (255, 255, 255, int(255 * alpha)))
    return Image.alpha_composite(img, overlay)


def _get_bg_color():
    return "#1e1e1e"


def _get_font(bold=False):
    system_fonts = {
        "Windows": ("Segoe UI", 12, "bold" if bold else "normal"),
        "Darwin": ("Helvetica", 12, "bold" if bold else "normal"),
        "Linux": ("Sans", 12, "bold" if bold else "normal"),
    }
    return system_fonts.get(
        platform.system(), ("Arial", 12, "bold" if bold else "normal")
    )


def _get_default_directory():
    return os.path.expanduser("~")


def _get_default_output_dir():
    return os.getcwd()
