import os
import sys
import pytest
import tkinter as tk
from app.gui import _resolve_image_path, _get_default_directory, _get_font


def test_resolve_image_path(tmp_path, monkeypatch):
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    (images_dir / "background.png").write_text("dummy content")

    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)

    result = _resolve_image_path("background.png")
    assert result is not None and os.path.basename(result) == "background.png"


def test_get_default_directory():
    assert os.path.exists(_get_default_directory())


def test_get_font():
    assert isinstance(_get_font(), tuple)
    assert isinstance(_get_font(bold=True), tuple)


@pytest.fixture
def gui_root():
    root = tk.Tk()
    root.withdraw()
    yield root
    root.quit()


def test_tkinter_root(gui_root):
    assert isinstance(gui_root, tk.Tk)
