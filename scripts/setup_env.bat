@echo off
echo ==========================================================
echo    ARMOR ENTERPRISE - VIRTUAL ENVIRONMENT SETUP           
echo ==========================================================

echo [1/3] Creating Python Virtual Environment (venv)...
python -m venv venv

echo [2/3] Upgrading pip inside virtual environment...
venv\Scripts\python.exe -m pip install --upgrade pip

echo [3/3] Installing enterprise dependencies from requirements.txt...
venv\Scripts\python.exe -m pip install -r requirements.txt

echo ==========================================================
echo  [SUCCESS] Virtual environment created and ready!
echo    To activate: venv\Scripts\activate.bat
echo    To run migrations: venv\Scripts\python.exe manage.py migrate
echo    To start dev server: venv\Scripts\python.exe manage.py runserver
echo ==========================================================
pause
