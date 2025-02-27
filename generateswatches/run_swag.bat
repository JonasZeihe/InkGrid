@echo off
:: Set the Python executable path if necessary
:: You can modify the path to Python if it's not in your system's PATH
set PYTHON_PATH=python

:: Run the Python script
%PYTHON_PATH% generate_swatches.py

pause
