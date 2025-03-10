#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

"""
Runs all tests for the InkGrid application with coverage.
"""

import os
import sys
import subprocess


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    os.chdir(root)

    if not os.path.isdir("venv"):
        print("No virtual environment found. Please initialize the project first.")
        input("Press Enter to exit...")
        sys.exit(1)

    _ensure_coverage_installed()
    print("Running tests with coverage...")
    _run_in_venv(
        [
            "coverage",
            "run",
            "--source=app",
            "-m",
            "unittest",
            "discover",
            "-s",
            "src/tests",
            "-p",
            "test_*.py",
        ]
    )
    _run_in_venv(["coverage", "report", "-m"])

    print()
    print("Tests completed. Press Enter to exit...")
    input()


def _ensure_coverage_installed():
    if os.name == "nt":
        act = os.path.join("venv", "Scripts", "activate.bat")
        show_cmd = f'call "{act}" && python -m pip show coverage'
        result = subprocess.run(show_cmd, shell=True, capture_output=True, text=True)
        if "Name: coverage" not in result.stdout:
            _install_coverage(activate_bat=act)
    else:
        act = "./venv/bin/activate"
        show_cmd = f'. "{act}" && python -m pip show coverage'
        result = subprocess.run(show_cmd, shell=True, capture_output=True, text=True)
        if "Name: coverage" not in result.stdout:
            _install_coverage(activate_sh=act)


def _install_coverage(activate_bat=None, activate_sh=None):
    print("Coverage not found. Installing...")
    if activate_bat:
        cmd = f'call "{activate_bat}" && python -m pip install coverage'
    else:
        cmd = f'. "{activate_sh}" && python -m pip install coverage'
    subprocess.run(cmd, shell=True, check=True)


def _run_in_venv(cmd):
    if os.name == "nt":
        act = os.path.join("venv", "Scripts", "activate.bat")
        full_cmd = f'call "{act}" && ' + " ".join(cmd)
        subprocess.run(full_cmd, shell=True, check=True)
    else:
        act = "./venv/bin/activate"
        joined = " ".join(cmd)
        full_cmd = f'. "{act}" && {joined}'
        subprocess.run(full_cmd, shell=True, check=True)


if __name__ == "__main__":
    main()
