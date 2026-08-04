@echo off

cd /d "%~dp0\.."

call .venv\Scripts\activate

python -m pip install --upgrade pip

pip install -U -r requirements.txt

pause