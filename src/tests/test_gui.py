import os
import sys
import pytest
import platform
from app.gui import _resolve_image_path, _get_default_directory, _get_font


def test_get_default_directory():
    default_dir = _get_default_directory()
    assert isinstance(default_dir, str)
    assert len(default_dir) > 0


def test_resolve_image_path(tmp_path, monkeypatch):
    import sys
    import os

    images_dir = tmp_path / "images"
    images_dir.mkdir()
    dummy_file = images_dir / "background.png"
    dummy_file.write_text("dummy content")

    monkeypatch.setitem(sys.__dict__, "frozen", True)
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path))

    from app.gui import _resolve_image_path

    result = _resolve_image_path("background.png")
    assert result is not None
    assert os.path.basename(result) == "background.png"


def test_get_font():
    font_normal = _get_font(bold=False)
    font_bold = _get_font(bold=True)
    assert isinstance(font_normal, tuple) and len(font_normal) == 3
    assert isinstance(font_bold, tuple) and len(font_bold) == 3
