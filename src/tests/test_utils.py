import os
import tempfile
import pytest
from app.utils import read_color_file, sanitize_id


def test_read_color_file_valid():
    content = "Primary: #FF5733\nSecondary: #33FF57\n# Kommentar\nTertiary: #3357FF"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    colors = read_color_file(tmp_path)
    os.remove(tmp_path)
    assert len(colors) == 3
    for group, color in colors:
        assert isinstance(group, str)
        assert color.startswith("#") and len(color) == 7


def test_read_color_file_invalid_path():
    colors = read_color_file("nonexistent_file.txt")
    assert colors == []


def test_read_color_file_ignore_comments():
    content = (
        "#Kommentarzeile\nPrimary: #FF5733\n# Noch ein Kommentar\nSecondary: #33FF57"
    )
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    colors = read_color_file(tmp_path)
    os.remove(tmp_path)
    for group, _ in colors:
        assert not group.strip().startswith("#")


def test_sanitize_id():
    assert sanitize_id("Some Group") == "Some_Group"
    assert sanitize_id("123 Group!") == "123_Group"
