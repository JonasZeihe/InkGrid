#!/usr/bin/env bash
# ----------------------------------------------------------------------
# Update Requirements Script
# Generates or updates the requirements.txt file based on the active
# virtual environment.
# 
# Copyright (c) 2025 Jonas Zeihe 
# Licensed under the MIT License. See LICENSE file in the project root.
# 
# Contact: JonasZeihe@gmail.com
# ----------------------------------------------------------------------

if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found! Please initialize the project first."
    echo "Press any key to exit..."
    read -n 1 -s
    exit 1
fi

source venv/bin/activate

echo "Updating requirements.txt..."
pip freeze > requirements.txt

echo
echo "requirements.txt has been updated successfully."
echo "Press any key to deactivate the virtual environment and close this window..."
read -n 1 -s

deactivate
