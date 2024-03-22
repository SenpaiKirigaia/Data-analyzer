@echo off

REM Get the current user's profile directory
set "CURRENT_USER=%USERPROFILE%"

REM Install Miniconda
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
start /wait "" miniconda.exe /S
del miniconda.exe

REM Open anaconda prompt and instal requirements
set ENVPATH=%CURRENT_USER%\miniconda3
call %ENVPATH%\Scripts\activate.bat %ENVPATH%
pip install -r requirements.txt
