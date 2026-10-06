@echo off
setlocal
title Streamlit App Launcher

REM Always run from the folder where this file is located.
cd /d "%~dp0"

REM Prefer the Windows Python launcher if available.
where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    set "PY=python"
)

echo.
echo ==========================================
echo   Starting app from:
echo   %CD%
echo ==========================================
echo.

REM Install/update required packages. On later runs this is usually very quick.
if exist "requirements.txt" (
    echo Checking required packages...
    %PY% -m pip install -r requirements.txt --disable-pip-version-check -q
    if errorlevel 1 (
        echo.
        echo Could not install the required packages.
        echo Make sure Python is installed and connected to the internet.
        echo.
        pause
        exit /b 1
    )
) else (
    echo Warning: requirements.txt was not found in this folder.
)

if not exist "app.py" (
    echo.
    echo app.py was not found in this folder.
    echo Put RUN_APP.bat in the same folder as app.py.
    echo.
    pause
    exit /b 1
)

echo.
echo Opening the app in your browser...
echo To stop it later, close this window or press Ctrl+C.
echo.

%PY% -m streamlit run app.py

echo.
echo The app has stopped.
pause
