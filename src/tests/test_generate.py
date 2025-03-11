"""
Tests for the SVG generation module in app.generate.
"""

import os
import tempfile
import pytest
from collections import OrderedDict
from unittest.mock import MagicMock
from svgwrite import Drawing
from app.generate import (
    generate_svg_from_groups,
    add_swatch,
    calculate_content_dimensions,
    SWATCH_WIDTH,
    HORIZONTAL_PADDING,
)


@pytest.fixture
def sample_colors():
    """
    Returns a sample list of colors as tuples (main_group, full_label, hex_color).
    """
    return [
        ("Primary", "Primary 1 (Main)", "#FF5733"),
        ("Secondary", "Secondary 1", "#33FF57"),
        ("Tertiary", "Tertiary 1", "#3357FF"),
        ("Primary", "Primary 2", "#F2F2F2"),
    ]


def test_generate_svg_creates_file(sample_colors, monkeypatch):
    """
    Checks that generate_svg_from_groups creates an SVG file by calling the save() method.
    """
    dummy_dwg = Drawing("dummy.svg")
    dummy_dwg.add = MagicMock()
    dummy_dwg.save = MagicMock()
    monkeypatch.setattr(
        "app.generate.svgwrite.Drawing", lambda *args, **kwargs: dummy_dwg
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "output.svg")
        generate_svg_from_groups(sample_colors, "dummy.txt", output_file=output_file)
        dummy_dwg.save.assert_called_once()


def test_add_swatch():
    """
    Ensures that add_swatch creates a swatch group with a sanitized ID and exactly three child elements.
    """
    drawing = Drawing()
    group = drawing.g()
    add_swatch(group, drawing, "Test Group", "#123456", 10, 20, "black")
    assert len(group.elements) == 1
    swatch_group = group.elements[0]
    assert "Test_Group" in swatch_group.attribs.get("id", "")
    assert len(swatch_group.elements) == 3


def test_calculate_content_dimensions():
    """
    Tests calculate_content_dimensions with multiple groups.
    """
    grouped = OrderedDict()
    grouped["Primary"] = ["#FFFFFF", "#F0F0F0"]
    grouped["Secondary"] = ["#000000", "#111111", "#222222", "#333333"]
    content_width, content_height = calculate_content_dimensions(grouped)
    expected_width = 4 * SWATCH_WIDTH + (4 - 1) * HORIZONTAL_PADDING
    assert content_width == expected_width
    assert content_height > 0
