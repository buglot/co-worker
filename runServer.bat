@echo off

:: Check if the co-worklib folder exists
IF NOT EXIST co-worklib (
    echo "co-worklib folder not found. Creating virtual environment..."
    python -m venv co-worklib
)

:: Activate the virtual environment
call co-worklib\Scripts\activate.bat

:: Install dependencies from requirements.txt
pip install -r requirements.txt

:: Run the Python server
python Server.py

:: Keep the command prompt open if you want to see the output
pause
