# Check if the co-worklib folder exists
if (-Not (Test-Path -Path "co-worklib")) {
    Write-Output "co-worklib folder not found. Creating virtual environment..."
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    python -m venv co-worklib
}

# Activate the virtual environment
& "co-worklib\Scripts\Activate.ps1"

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run the Python server
python Server.py
