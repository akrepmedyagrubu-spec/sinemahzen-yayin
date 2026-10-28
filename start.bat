@echo off
python -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
if errorlevel 1 exit /b 1
python stream.py
