@echo off
REM ----------------------------------------------------------------------
REM Universal Project Initializer & Refresher
REM Initializes or updates the virtual environment and dependencies.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Check if the virtual environment exists, otherwise create it
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Ensure pip is up to date
echo Checking for pip updates...
python -m pip install --upgrade pip

REM Install or update dependencies only if requirements.txt exists
IF EXIST requirements.txt (
    echo Installing/updating dependencies...
    python -m pip install --no-cache-dir -r requirements.txt
) ELSE (
    echo WARNING: No requirements.txt found. Skipping dependency installation.
)

REM Check for missing Python modules and install them dynamically
for %%m in (PIL svgwrite) do (
    python -c "import %%m" 2>nul || (
        echo %%m is missing. Installing...
        python -m pip install %%m
    )
)

REM Synchronize requirements.txt with installed packages
echo Updating requirements.txt...
python -m pip freeze > requirements.txt

REM Completion message
echo Initialization & refresh complete!
echo Press any key to deactivate the virtual environment and exit...
pause > nul

REM Properly deactivate the virtual environment
echo Deactivating virtual environment...
call venv\Scripts\deactivate.bat 2>nul || echo No deactivate command found.
