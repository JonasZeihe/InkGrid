# tests/test_utils.py

import pytest
from inkgrid.utils import read_color_file, sanitize_id

def test_read_color_file_valid():
    colors = read_color_file("tests/data/valid_colors.txt")
    assert len(colors) > 0
    assert all(len(color) == 2 for color in colors)  # Each color is a tuple of (group, hex color)

def test_read_color_file_invalid_path():
    colors = read_color_file("invalid_path.txt")
    assert colors == []  # Expects empty list if file is not found

def test_read_color_file_ignore_comments():
    colors = read_color_file("tests/data/with_comments.txt")
    assert all(not color[1].startswith("#") for color in colors)

def test_sanitize_id():
    assert sanitize_id("Some Group") == "Some_Group"
    assert sanitize_id("123 Group!") == "123_Group"
