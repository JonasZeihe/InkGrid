# tests/test_gui.py

from unittest.mock import patch
from inkgrid.gui import select_color_file

@patch("tkinter.filedialog.askopenfilename")
def test_select_color_file(mock_askopenfilename):
    # Simulate selecting a file
    mock_askopenfilename.return_value = "test_colors.txt"
    file_path = select_color_file()
    assert file_path == "test_colors.txt"

@patch("tkinter.filedialog.askopenfilename")
def test_select_color_file_cancel(mock_askopenfilename):
    # Simulate cancelling the file dialog
    mock_askopenfilename.return_value = ""
    file_path = select_color_file()
    assert file_path is None
