@echo off
REM (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

cd /d %~dp0
cd ..\..
python scripts\logic\test_all.py
