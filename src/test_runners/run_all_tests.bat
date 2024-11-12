@echo off
REM -----------------------------------------------------------------------------
REM InkGrid - A tool for creating and managing color swatches for design projects
REM 
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/yourusername/inkgrid
REM Contact: your.email@example.com
REM -----------------------------------------------------------------------------

@echo off
cls

REM Set the working directory to the project root (one level above the test_runners folder)
cd /d %~dp0..\

REM Run all tests with coverage
echo Running all tests with coverage...

coverage run --source=inkgrid -m unittest discover -s tests -p "test_*.py"
coverage report -m

echo.
echo Coverage report complete. Check the HTML report for detailed results in the 'htmlcov' directory.
echo Press any key to exit...
pause > nul
