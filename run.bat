@echo off
echo ============================================================
echo Restaurant Order Management API - Startup Script
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then activate it and install requirements.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo Virtual environment activated successfully!
echo.

REM Run the API server
echo Starting API server...
echo.
echo API will be available at:
echo   - Interactive Docs: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo   - Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
