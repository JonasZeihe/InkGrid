@echo off
REM -----------------------------------------------------------------------------
REM InkGrid - A tool for creating and managing color swatches for design projects
REM 
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/yourusername/inkgrid
REM Contact: your.email@example.com
REM -----------------------------------------------------------------------------

REM Check if at least one argument (file) is provided
if "%~1"=="" (
    echo No file provided. Please drag and drop a color file (.txt) onto this batch script.
    pause
    exit /b 1
)

REM Running InkGrid with the provided file(s) and logging enabled
echo Running InkGrid with logging...
python src/main.py --logging %*

REM Pause to keep the window open until the user presses a key
echo.
echo Press any key to exit...
pause > nul
