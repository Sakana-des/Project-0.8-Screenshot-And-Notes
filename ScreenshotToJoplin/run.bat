@echo off
echo Setting up environment for Screenshot to Joplin...
if not exist venv (
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)
echo Starting Application...
python main.py
pause
