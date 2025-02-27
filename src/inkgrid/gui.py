import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from inkgrid.utils import read_color_file
from inkgrid.generate import generate_svg

def run_app():
    root = tk.Tk()
    root.title("InkGrid")
    root.geometry("400x250")
    root.configure(bg="#2b2b2b")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#2b2b2b")
    style.configure("TLabel", background="#2b2b2b", foreground="white", font=("Arial", 12))
    style.configure("TButton", background="#444", foreground="white", font=("Arial", 12))
    style.map("TButton", background=[("active", "#555")])

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="InkGrid - SVG Generator", font=("Arial", 14, "bold")).pack(pady=10)

    selected_file_var = tk.StringVar(value="No file selected")

    file_frame = ttk.LabelFrame(frame, text="File Selection", padding=10)
    file_frame.pack(fill="x", padx=10, pady=10)

    file_label = ttk.Label(file_frame, textvariable=selected_file_var)
    file_label.pack(side="left", padx=10)

    ttk.Button(file_frame, text="Browse", command=lambda: select_file(selected_file_var)).pack(side="right", padx=10)

    ttk.Button(frame, text="Generate SVG", command=lambda: generate(selected_file_var)).pack(pady=15)

    root.mainloop()

def select_file(selected_file_var):
    path = filedialog.askopenfilename(
        title="Select color file",
        filetypes=[("Text Files", "*.txt")]
    )
    if path:
        selected_file_var.set(path)

def generate(selected_file_var):
    path = selected_file_var.get()
    if path != "No file selected":
        colors = read_color_file(path)
        if colors:
            generate_svg(colors, path)
            messagebox.showinfo("Success", "SVG successfully generated!")
        else:
            messagebox.showerror("Error", "No valid colors found in the file.")
    else:
        messagebox.showwarning("Warning", "No file selected")
