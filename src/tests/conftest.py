# tests/conftest.py

import pytest
import os

@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    os.makedirs("tests/data", exist_ok=True)
    with open("tests/data/valid_colors.txt", "w") as f:
        f.write("Primary: #FF5733\nSecondary: #33FF57\nTertiary: #3357FF\n")
    with open("tests/data/with_comments.txt", "w") as f:
        f.write("# This is a comment\nPrimary: #FF5733\n# Another comment\nSecondary: #33FF57\n")
