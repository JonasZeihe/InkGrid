# src/tests/test_export.py

import os
import tempfile
import json
from app.export import export_json_for_figma


def test_export_json_for_figma_creates_valid_json():
    colors = [
        ("Primary", "Primary 1", "#FF0000"),
        ("Primary", "Primary 2", "#00FF00"),
        ("Secondary", "Secondary 1", "#0000FF"),
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "colors.txt")
        with open(input_file, "w") as f:
            f.write("dummy")

        json_path = export_json_for_figma(colors, input_file, tmpdir)
        assert os.path.exists(json_path)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "Primary" in data
        assert "Secondary" in data
        assert data["Primary"]["Primary 1"] == "#FF0000"
        assert data["Primary"]["Primary 2"] == "#00FF00"
        assert data["Secondary"]["Secondary 1"] == "#0000FF"
