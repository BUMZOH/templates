@echo off

REM Move current directory
cd /d %~dp0

REM Run application
python main.py

REM Pause for error check
pause