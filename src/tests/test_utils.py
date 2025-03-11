"""
Tests for utility functions in app.utils.
"""

import os
import tempfile
import pytest
from app.utils import read_color_file, sanitize_id


def test_read_color_file_valid():
    """
    Checks that read_color_file returns a list of tuples (main_group, full_label, hex_color) for valid input.
    """
    content = "Primary 1: #FF5733\nSecondary 1: #33FF57\nTertiary 1: #3357FF"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    colors = read_color_file(tmp_path)
    os.remove(tmp_path)
    assert len(colors) == 3
    for item in colors:
        main_group, full_label, color = item
        assert isinstance(main_group, str)
        assert isinstance(full_label, str)
        assert color.startswith("#") and len(color) == 7


def test_read_color_file_invalid_path():
    """
    Checks that read_color_file returns an empty list for a nonexistent file.
    """
    colors = read_color_file("nonexistent_file.txt")
    assert not colors


def test_read_color_file_ignore_comments():
    """
    Checks that read_color_file ignores comment and empty lines.
    """
    content = "# Kommentarzeile\nPrimary 1: #FF5733\n# Noch ein Kommentar\nSecondary 1: #33FF57"
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    colors = read_color_file(tmp_path)
    os.remove(tmp_path)
    for item in colors:
        main_group, full_label, _ = item
        assert not main_group.strip().startswith("#")


def test_sanitize_id():
    """
    Checks that sanitize_id replaces non-alphanumeric characters with underscores.
    """
    assert sanitize_id("Some Group") == "Some_Group"
    assert sanitize_id("123 Group!") == "123_Group"
