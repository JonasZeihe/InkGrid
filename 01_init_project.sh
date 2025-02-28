#!/usr/bin/env bash
# ----------------------------------------------------------------------
# Enhanced Project Initializer
# Ensures complete dependency tracking and synchronization.
# Copyright (c) 2025 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
# 
# Contact: JonasZeihe@gmail.com
# ----------------------------------------------------------------------

set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv --system-site-packages
else
    echo "Virtual environment already exists."
fi

source venv/bin/activate

echo "Upgrading pip to the latest version..."
pip install --upgrade pip

if ! pip show pipreqsnb >/dev/null 2>&1; then
    echo "Installing pipreqsnb for dependency detection..."
    pip install pipreqsnb
fi

echo "Generating full dependency list from source code..."
pipreqsnb . --force --ignore venv

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Checking for missing standard modules..."
if ! python -c "import tkinter" &>/dev/null; then
    echo "Tkinter is missing. Installing Tcl-Tk..."
    brew install python-tk
    echo 'export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"' >> venv/bin/activate
    echo 'export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"' >> venv/bin/activate
    echo 'export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"' >> venv/bin/activate
    echo 'export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"' >> venv/bin/activate
    source venv/bin/activate
fi

echo "Finalizing dependencies..."
pip freeze > requirements.txt

echo "Virtual environment setup complete."
read -n 1 -s
deactivate
