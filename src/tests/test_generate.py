import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from app.generate import generate_svg, calculate_positions, add_swatch


@pytest.fixture
def sample_colors():
    return [("Primary", "#FF5733"), ("Secondary", "#33FF57"), ("Tertiary", "#3357FF")]


def test_generate_svg_creates_file(sample_colors, monkeypatch):
    mock_dwg = MagicMock()
    monkeypatch.setattr(
        "app.generate.svgwrite.Drawing", lambda *args, **kwargs: mock_dwg
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "output.svg")
        generate_svg(sample_colors, "dummy.txt", output_file=output_file)
        mock_dwg.save.assert_called_once()


def test_calculate_positions():
    margin = 40
    padding = 20
    swatch_size = (120, 120)
    text_height = 20
    text_padding_top = 40
    content_height = 300

    x, y_top, y_bottom = calculate_positions(
        0, margin, padding, swatch_size, text_height, text_padding_top, content_height
    )
    expected_x = margin + padding  # Spalte 0
    expected_y_top = margin + padding + text_padding_top
    expected_y_bottom = expected_y_top + content_height + 80

    assert x == expected_x
    assert y_top == expected_y_top
    assert y_bottom == expected_y_bottom


def test_add_swatch():
    from svgwrite import Drawing
    from app.generate import add_swatch

    dwg = Drawing()
    group = dwg.g()
    add_swatch(group, dwg, "Test Group", "#123456", 10, 20, "black")

    swatch_group = group.elements[0]
    assert swatch_group.attribs.get("id") == "Test_Group"
    assert len(swatch_group.elements) == 3
