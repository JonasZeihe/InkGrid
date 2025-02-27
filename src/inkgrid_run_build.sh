#!/usr/bin/env bash

set -e
cd "$(dirname "$0")"

VENV_PATH="../venv"
SCRIPT_PATH="main.py"
OUTPUT_NAME="InkGrid"

if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Initializing..."
    bash ../01_init_project.sh
fi

source "$VENV_PATH/bin/activate"

if ! command -v pyinstaller &>/dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

rm -rf build dist

echo "Building $OUTPUT_NAME..."
pyinstaller --onefile --name "$OUTPUT_NAME" --clean "$SCRIPT_PATH"

echo "Build complete. Executable in 'dist' folder."
deactivate
