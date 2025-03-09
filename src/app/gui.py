"""
GUI for InkGrid. Lets the user pick a color file and output folder,
generates an SVG, and creates a matching log file if logging is enabled.
"""

import os
import platform
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from app.generate import generate_svg
from app.utils import read_color_file
from app.logger_config import setup_logger


def run_app(logging_enabled=False):
    """
    Starts the GUI. If logging_enabled is True, logs go to a file named alongside the SVG.
    """
    root = tk.Tk()
    root.title("InkGrid - SVG Generator")
    root.geometry("680x460")
    root.resizable(False, False)
    root.configure(bg=_get_bg_color())

    bg_image = _get_background_image()
    if bg_image:
        canvas = tk.Canvas(root, width=680, height=460, highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")

    _apply_theme(root)

    frame = ttk.Frame(root, padding=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="InkGrid - SVG Generator", font=_get_font(bold=True)).pack(
        pady=10
    )

    selected_file_var = tk.StringVar(value="No file selected")
    output_folder_var = tk.StringVar(value="No folder selected")

    file_frame = ttk.LabelFrame(frame, text="Color File", padding=10)
    file_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(file_frame, textvariable=selected_file_var).pack(side="left", padx=10)
    ttk.Button(
        file_frame, text="Browse", command=lambda: _select_file(selected_file_var)
    ).pack(side="right", padx=10)

    folder_frame = ttk.LabelFrame(frame, text="Output Folder", padding=10)
    folder_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(folder_frame, textvariable=output_folder_var).pack(side="left", padx=10)
    ttk.Button(
        folder_frame, text="Choose", command=lambda: _select_folder(output_folder_var)
    ).pack(side="right", padx=10)

    ttk.Button(
        frame,
        text="Generate SVG",
        command=lambda: _generate(
            root, selected_file_var, output_folder_var, logging_enabled
        ),
    ).pack(pady=15)

    root.mainloop()


def _generate(root, file_var, folder_var, logging_enabled):
    path = file_var.get()
    out_dir = folder_var.get()
    if path == "No file selected":
        messagebox.showwarning("Warning", "No color file selected.")
        return
    if out_dir == "No folder selected":
        out_dir = _get_default_output_dir()

    colors = read_color_file(path)
    if not colors:
        messagebox.showerror("Error", "No valid colors found in the file.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(path))[0]
    svg_name = f"{timestamp}_{base_name}.svg"
    log_name = f"{timestamp}_{base_name}.log"

    os.makedirs(out_dir, exist_ok=True)
    svg_path = os.path.join(out_dir, svg_name)
    log_path = os.path.join(out_dir, log_name)

    if logging_enabled:
        setup_logger(to_file=True, log_file=log_path)

    generate_svg(colors, path, output_file=svg_path)

    msg = f"SVG created:\n{svg_path}"
    if logging_enabled:
        msg += f"\n\nLog file:\n{log_path}"
    msg += "\n\nGenerate another file?"
    if messagebox.askyesno("Success", msg):
        file_var.set("No file selected")
    else:
        root.destroy()


def _select_file(selected_file_var):
    path = filedialog.askopenfilename(
        title="Select color file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        initialdir=_get_default_directory(),
    )
    if path:
        selected_file_var.set(path)


def _select_folder(folder_var):
    path = filedialog.askdirectory(title="Select output folder")
    if path:
        folder_var.set(path)


def _apply_theme(root):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background=_get_bg_color())
    style.configure(
        "TLabel", background=_get_bg_color(), foreground="white", font=_get_font()
    )
    style.configure(
        "TButton", background=_get_button_color(), foreground="white", font=_get_font()
    )
    style.map("TButton", background=[("active", _get_button_hover_color())])


def _get_background_image():
    image_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "images", "inkgrid_logo.png"
    )
    if not os.path.exists(image_path):
        return None
    img = Image.open(image_path).convert("RGBA")
    img = img.resize((680, 460), Image.LANCZOS)
    img = _adjust_opacity(img, 0.6)
    return ImageTk.PhotoImage(img)


def _adjust_opacity(img, alpha):
    overlay = Image.new("RGBA", img.size, (255, 255, 255, int(255 * alpha)))
    return Image.alpha_composite(img, overlay)


def _get_bg_color():
    return "#2b2b2b" if platform.system() == "Windows" else "#333"


def _get_button_color():
    return "#444" if platform.system() == "Windows" else "#555"


def _get_button_hover_color():
    return "#555" if platform.system() == "Windows" else "#666"


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
    if platform.system() == "Windows":
        return os.path.expanduser("~/Documents")
    elif platform.system() == "Darwin":
        return os.path.expanduser("~/Desktop")
    return os.path.expanduser("~")


def _get_default_output_dir():
    """
    If no folder is chosen, fallback to Desktop or Documents,
    or any path you'd like as a default output.
    """
    if platform.system() == "Windows":
        return os.path.expanduser("~/Documents/InkGrid_Output")
    elif platform.system() == "Darwin":
        return os.path.expanduser("~/Desktop/InkGrid_Output")
    return os.path.expanduser("~/InkGrid_Output")
