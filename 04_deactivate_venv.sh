#!/usr/bin/env bash
# ----------------------------------------------------------------------
# Virtual Environment Deactivator
# Deactivates the virtual environment if it is currently active.
# 
# Licensed under the MIT License. See LICENSE file in the project root.
#
# Copyright (c) 2025 Jonas Zeihe 
# 
# Contact: JonasZeihe@gmail.com
# ----------------------------------------------------------------------

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Nothing to deactivate."
    read -n 1 -s
    exit 0
fi

echo "Attempting to deactivate the virtual environment..."

if [[ -n "$VIRTUAL_ENV" ]]; then
    deactivate
    echo "Virtual environment deactivated successfully!"
else
    echo "No active virtual environment found to deactivate."
fi

read -n 1 -s
exit 0
