#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

"""
Build script for creating a standalone executable of the application
via PyInstaller or similar tools.
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

    _run_in_venv(["python", "-m", "pip", "show", "pyinstaller"], check_install=True)

    dist_path = os.path.join(root, "dist")
    build_path = os.path.join(root, "build")

    if os.path.isdir(dist_path):
        _rmdir(dist_path)
    if os.path.isdir(build_path):
        _rmdir(build_path)

    image_path = os.path.join(root, "images", "background.png")
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--name",
        "Application",
        "src/app/main.py",
    ]

    if os.path.exists(image_path):
        if os.name == "nt":
            pyinstaller_cmd.append(f"--add-data={image_path};images")
        else:
            pyinstaller_cmd.append(f"--add-data={image_path}:images")

    print("Building with PyInstaller...")
    _run_in_venv(pyinstaller_cmd)

    print("Build complete. Executable is in 'dist' folder.")


def _run_in_venv(cmd, check_install=False):
    """
    Runs a command inside the virtual environment. If check_install=True and
    the module isn't installed, it installs it before continuing.
    """
    if os.name == "nt":
        activate = os.path.join("venv", "Scripts", "activate.bat")
        if check_install and "show" in cmd:
            show_cmd = f'call "{activate}" && ' + " ".join(cmd)
            ret = subprocess.run(show_cmd, shell=True, capture_output=True, text=True)
            if "Name: PyInstaller" not in ret.stdout:
                _install_pyinstaller(activate)
        run_cmd = f'call "{activate}" && ' + " ".join(cmd)
        subprocess.run(run_cmd, shell=True, check=True)
    else:
        activate = "./venv/bin/activate"
        if check_install and "show" in cmd:
            joined = " ".join(cmd)
            show_cmd = f'. "{activate}" && {joined}'
            ret = subprocess.run(show_cmd, shell=True, capture_output=True, text=True)
            if "Name: PyInstaller" not in ret.stdout:
                _install_pyinstaller(activate)
        run_cmd = f'. "{activate}" && {" ".join(cmd)}'
        subprocess.run(run_cmd, shell=True, check=True)


def _install_pyinstaller(activate):
    print("PyInstaller not found. Installing...")
    if os.name == "nt":
        install_cmd = f'call "{activate}" && python -m pip install pyinstaller'
    else:
        install_cmd = f'. "{activate}" && python -m pip install pyinstaller'
    subprocess.run(install_cmd, shell=True, check=True)


def _rmdir(path):
    if os.path.isdir(path):
        print(f"Removing {path}...")
        if os.name == "nt":
            subprocess.run(["rmdir", "/s", "/q", path], shell=True, check=True)
        else:
            subprocess.run(["rm", "-rf", path], check=True)


if __name__ == "__main__":
    main()
