@echo off

cd /d "%~dp0\.."

call .venv\Scripts\activate

python 11_SCRIPT\app.py

if errorlevel 1 (
    echo.
    echo ============================================
    echo APPLICATION TERMINATED WITH ERROR
    echo ============================================
)

pause
