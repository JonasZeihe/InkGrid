"""
Tests for the GUI helper functions in app.gui.
"""

import os
import sys
import tkinter as tk
from tkinter.ttk import LabelFrame, Style
import pytest
from app.gui import (
    _resolve_image_path,
    _get_default_directory,
    _get_font,
    _adjust_opacity,
    _get_background_image,
    _create_file_selection,
    _create_folder_selection,
    _select_files,
    _select_folder,
    _apply_theme,
    _get_bg_color,
)


@pytest.fixture
def gui_root():
    """
    Provides a Tkinter root window and destroys it after the test.
    Skips tests if Tcl is not properly installed.
    """
    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError as e:
        pytest.skip("Tcl is not available: " + str(e))
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass


def test_resolve_image_path(tmp_path, monkeypatch):
    """
    Tests that _resolve_image_path returns the correct image path.
    """
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    (images_dir / "background.png").write_text("dummy content")
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
    result = _resolve_image_path("background.png")
    assert result is not None and os.path.basename(result) == "background.png"


def test_get_default_directory():
    """
    Tests that _get_default_directory returns an existing directory.
    """
    assert os.path.exists(_get_default_directory())


def test_get_font():
    """
    Ensures that _get_font returns a tuple for both normal and bold fonts.
    """
    font_normal = _get_font()
    font_bold = _get_font(bold=True)
    assert isinstance(font_normal, tuple)
    assert isinstance(font_bold, tuple)


def test_get_bg_color():
    """
    Tests that _get_bg_color returns the correct background color.
    """
    color = _get_bg_color()
    assert isinstance(color, str)
    assert color == "#1e1e1e"


def test_tkinter_root(gui_root):
    """
    Checks that the created GUI root is an instance of Tk.
    """
    assert isinstance(gui_root, tk.Tk)


def test_create_file_and_folder_selection(gui_root):
    """
    Tests that _create_file_selection and _create_folder_selection add appropriate widgets.
    """
    frame = tk.Frame(gui_root)
    selected_files_var = tk.StringVar(value="No files selected")
    output_folder_var = tk.StringVar(value="No folder selected")
    _create_file_selection(frame, selected_files_var)
    _create_folder_selection(frame, output_folder_var)
    label_frames = [
        child for child in frame.winfo_children() if isinstance(child, LabelFrame)
    ]
    assert len(label_frames) >= 2


def test_select_files(monkeypatch, gui_root):
    """
    Tests _select_files by monkey-patching filedialog.askopenfilenames.
    """
    fake_paths = ("file1.txt", "file2.txt")
    monkeypatch.setattr(
        "tkinter.filedialog.askopenfilenames", lambda **kwargs: fake_paths
    )
    selected_files_var = tk.StringVar(value="No files selected")
    _select_files(selected_files_var)
    assert selected_files_var.get() == "file1.txt;file2.txt"


def test_select_files_empty(monkeypatch, gui_root):
    """
    Tests _select_files when no file is selected.
    """
    monkeypatch.setattr("tkinter.filedialog.askopenfilenames", lambda **kwargs: ())
    selected_files_var = tk.StringVar(value="No files selected")
    _select_files(selected_files_var)
    assert selected_files_var.get() == "No files selected"


def test_select_folder(monkeypatch, gui_root):
    """
    Tests _select_folder by monkey-patching filedialog.askdirectory.
    """
    fake_folder = "C:/fake/folder"
    monkeypatch.setattr("tkinter.filedialog.askdirectory", lambda **kwargs: fake_folder)
    folder_var = tk.StringVar(value="No folder selected")
    _select_folder(folder_var)
    assert folder_var.get() == fake_folder


def test_select_folder_empty(monkeypatch, gui_root):
    """
    Tests _select_folder when no folder is selected.
    """
    monkeypatch.setattr("tkinter.filedialog.askdirectory", lambda **kwargs: "")
    folder_var = tk.StringVar(value="No folder selected")
    _select_folder(folder_var)
    assert folder_var.get() == "No folder selected"


def test_apply_theme(gui_root):
    """
    Tests _apply_theme by verifying that the theme is set to 'clam'.
    """
    _apply_theme(gui_root)
    style = Style()
    assert style.theme_use() == "clam"


def test_adjust_opacity():
    """
    Tests _adjust_opacity to ensure the output image has the same size and that its pixel values change.
    """
    from PIL import Image

    img = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
    result = _adjust_opacity(img, 0.5)
    assert result.size == img.size
    assert result.getpixel((50, 50)) != img.getpixel((50, 50))


def test_get_background_image(monkeypatch):
    """
    Tests _get_background_image by patching _resolve_image_path to return a valid image file.
    Ensures a default Tk root is created for PhotoImage.
    """
    from PIL import Image, ImageTk

    root = tk.Tk()
    root.withdraw()
    temp_img_path = os.path.join(os.getcwd(), "temp_background.png")
    img = Image.new("RGB", (720, 520), (0, 128, 255))
    img.save(temp_img_path)
    monkeypatch.setattr("app.gui._resolve_image_path", lambda filename: temp_img_path)
    bg_image = _get_background_image()
    os.remove(temp_img_path)
    root.destroy()
    assert isinstance(bg_image, ImageTk.PhotoImage)


def test_get_background_image_no_file(monkeypatch):
    """
    Tests _get_background_image when _resolve_image_path returns None.
    """
    monkeypatch.setattr("app.gui._resolve_image_path", lambda filename: None)
    bg_image = _get_background_image()
    assert bg_image is None
