@echo off
REM ============================================================
REM AppointmentPro Setup Script for Windows
REM This script helps set up the backend and frontend
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo        AppointmentPro Setup Script
echo ============================================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: backend folder not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo [OK] Project structure found
echo.

REM Create backend virtual environment
echo [1/5] Creating Python virtual environment...
cd backend
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install requirements
echo [3/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check for .env file
echo [4/5] Checking environment configuration...
if not exist ".env" (
    echo.
    echo WARNING: .env file not found
    echo.
    echo Please follow these steps:
    echo.
    echo 1. Go to https://console.firebase.google.com
    echo 2. Create a new project or select existing one
    echo 3. Enable Firestore Database and Authentication
    echo 4. Go to Project Settings ^> Service Accounts
    echo 5. Click "Generate New Private Key"
    echo 6. Save as firebase-key.json in the backend/ folder
    echo 7. Copy .env.example to .env
    echo 8. Fill in Firebase credentials from firebase-key.json
    echo.
    pause
) else (
    echo [OK] .env file found
)
echo.

REM Check for firebase-key.json
echo [5/5] Checking Firebase credentials...
if not exist "firebase-key.json" (
    echo.
    echo WARNING: firebase-key.json not found
    echo The app will run but Firebase features won't work
    echo.
    echo To enable Firebase:
    echo 1. Go to https://console.firebase.google.com
    echo 2. Go to Project Settings ^> Service Accounts
    echo 3. Click "Generate New Private Key"
    echo 4. Save as firebase-key.json in the backend/ folder
    echo.
    pause
) else (
    echo [OK] Firebase credentials found
)
echo.

REM Setup complete
echo ============================================================
echo        Setup Complete!
echo ============================================================
echo.
echo To start the backend:
echo   1. Run: setup.bat (this file)
echo   2. Run: python app.py
echo   3. Access: http://localhost:5000
echo.
echo To start the frontend:
echo   1. Open another terminal
echo   2. cd frontend
echo   3. python -m http.server 8000
echo   4. Open: http://localhost:8000
echo.
echo For more details, see README.md
echo.

pause
