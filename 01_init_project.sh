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
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip

if ! pip show pipreqsnb >/dev/null 2>&1; then
    pip install pipreqsnb
fi

pipreqsnb . --force --ignore venv
pip install -r requirements.txt

if ! python -c "import tkinter" &>/dev/null; then
    brew install python-tk
    echo 'export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"' >> venv/bin/activate
    echo 'export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"' >> venv/bin/activate
    echo 'export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"' >> venv/bin/activate
    echo 'export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"' >> venv/bin/activate
    source venv/bin/activate
fi

pip freeze | sed '/file:\/\//d' > requirements.txt

deactivate

