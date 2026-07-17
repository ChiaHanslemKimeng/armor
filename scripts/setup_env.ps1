# Armor Enterprise Platform - Virtual Environment Setup (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   ARMOR ENTERPRISE - VIRTUAL ENVIRONMENT SETUP           " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Write-Host "[1/3] Creating Python Virtual Environment (venv)..." -ForegroundColor Yellow
python -m venv venv

Write-Host "[2/3] Upgrading pip inside virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host "[3/3] Installing enterprise dependencies from requirements.txt..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Virtual environment created and ready!" -ForegroundColor Green
Write-Host "   To activate in PowerShell: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   To run migrations: .\venv\Scripts\python.exe manage.py migrate" -ForegroundColor White
Write-Host "   To start dev server: .\venv\Scripts\python.exe manage.py runserver" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green
