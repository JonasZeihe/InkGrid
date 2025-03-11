# src/tests/conftest.py
"""
Fügt das src-Verzeichnis dem sys.path hinzu, damit der Package-Import (app.*)
funktioniert.
"""
import os
import sys

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)
