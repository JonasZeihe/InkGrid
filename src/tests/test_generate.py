# tests/test_generate.py

import pytest
from inkgrid.generate import generate_svg
from unittest.mock import patch, MagicMock

def test_generate_svg_file_creation():
    colors = [("Primary", "#FF5733"), ("Secondary", "#33FF57")]
    with patch("svgwrite.Drawing.save") as mock_save:
        generate_svg(colors, input_filename="colors.txt")
        mock_save.assert_called_once()

@patch("inkgrid.generate.svgwrite.Drawing")
def test_generate_svg_content(mock_dwg):
    colors = [("Group1", "#FF5733"), ("Group2", "#33FF57")]
    generate_svg(colors, input_filename="test_colors.txt")
    
    # Verify calls within the generated SVG
    assert mock_dwg.call_count == 1  # Ensure an SVG Drawing object was created
    assert mock_dwg.return_value.add.call_count >= len(colors) * 2  # Each color gets two swatches (light & dark)
