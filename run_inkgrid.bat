@echo off
REM -----------------------------------------------------------------------------
REM InkGrid - A tool for creating and managing color swatches for design projects
REM 
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/yourusername/inkgrid
REM Contact: your.email@example.com
REM -----------------------------------------------------------------------------

cls

REM Running InkGrid without logging (For development purposes)
echo Running InkGrid without logging...
python src/main.py

REM Pause to keep the window open until the user presses a key
echo.
echo Press any key to exit...
pause > nul
