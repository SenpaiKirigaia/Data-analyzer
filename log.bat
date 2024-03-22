@echo off

REM Get the current user's profile directory
set "CURRENT_USER=%USERPROFILE%"

%CURRENT_USER%\miniconda3\python.exe %CURRENT_USER%\mitra\log-analyzer\log_analyzer.py %CURRENT_USER%\mitra\log-analyzer\send
pause