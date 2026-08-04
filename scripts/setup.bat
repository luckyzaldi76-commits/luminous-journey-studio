@echo off

echo ============================================
echo LUMINOUS JOURNEY INSTALLER
echo ============================================

cd /d "%~dp0\.."

echo.
echo Creating Virtual Environment...

python -m venv .venv

echo.
echo Activating...

call .venv\Scripts\activate

echo.
echo Upgrading pip...

python -m pip install --upgrade pip

echo.
echo Installing dependencies...

pip install -r requirements.txt

echo.
echo ============================================
echo INSTALLATION FINISHED
echo ============================================

pause