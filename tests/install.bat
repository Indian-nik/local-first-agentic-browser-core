@echo off
setlocal enabledelayedexpansion

echo ======================================
echo   CyberCore Installation Script
echo   Cross-Platform Security Framework
echo ======================================
echo.

REM Check if Python is installed
echo Checking for Python installation...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://python.org
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PYTHON_VERSION=%%V
echo [OK] Python %PYTHON_VERSION% detected

REM Check Python version (simplified check)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo [ERROR] Python 3.11+ required ^(found %PYTHON_VERSION%^)
    pause
    exit /b 1
)

if %MAJOR% EQU 3 if %MINOR% LSS 11 (
    echo [ERROR] Python 3.11+ required ^(found %PYTHON_VERSION%^)
    pause
    exit /b 1
)

echo.
echo Installation Options:
echo   1. Install in virtual environment ^(recommended^)
echo   2. Install system-wide
echo   3. Install in development mode
echo.
set /p option="Choose option [1-3]: "

if "%option%"=="1" (
    echo.
    echo Installing in virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip setuptools wheel
    pip install -e .
    echo.
    echo [OK] Installation complete!
    echo.
    echo To activate the environment, run:
    echo   venv\Scripts\activate.bat
    echo.
    echo Then you can use:
    echo   cybercore --help
    echo   cybercore-api
    echo   cybercore-optimize
) else if "%option%"=="2" (
    echo.
    echo Installing system-wide...
    pip install -e .
    echo.
    echo [OK] Installation complete!
    echo.
    echo You can now use:
    echo   cybercore --help
    echo   cybercore-api
    echo   cybercore-optimize
) else if "%option%"=="3" (
    echo.
    echo Installing in development mode...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip setuptools wheel
    pip install -e .[dev,docs]
    echo.
    echo [OK] Development installation complete!
    echo.
    echo To activate the environment, run:
    echo   venv\Scripts\activate.bat
    echo.
    echo Development tools installed:
    echo   - pytest, black, flake8, mypy
    echo   - sphinx for documentation
) else (
    echo [ERROR] Invalid option
    pause
    exit /b 1
)

echo.
echo For more information, see INSTALL.md
echo.
pause
