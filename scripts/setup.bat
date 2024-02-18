@echo off

python3 -m venv .venv
./.venv/Scripts/activate.bat
pip install -r requirements.txt
flask --app ./sudoku init-db