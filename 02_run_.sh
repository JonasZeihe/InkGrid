#!/usr/bin/env bash
# ----------------------------------------------------------------------
# Universal Run Script
# Runs the application within its virtual environment.
#
# Copyright (c) 2025 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Developer: Jonas Zeihe
# Contact: JonasZeihe@gmail.com
# ----------------------------------------------------------------------

set -e

cd "$(dirname "$0")"

if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found! Please initialize the project first."
    exit 1
fi

source venv/bin/activate

export PYTHONPATH="$(pwd)/src"

echo "Running the application..."
python -m main "$@"

echo "Execution complete. Press any key to exit..."
read -n 1 -s

deactivate

