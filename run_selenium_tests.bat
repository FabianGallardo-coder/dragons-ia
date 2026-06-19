@echo off
REM Selenium Test Runner for Dragons & IA
REM This script helps run the Selenium tests for the frontend

echo.
echo ================================================
echo   Dragons & IA - Selenium Test Runner
echo ================================================
echo.

REM Check if virtual environment exists, if so activate it
if exist venv\Scripts\activate (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else if exist venv\bin\activate (
    echo Activating virtual environment...
    source venv\bin\activate
) else (
    echo No virtual environment found. Using system Python.
)

REM Check if selenium is installed, if not install it
python -c "import selenium" 2>nul
if errorlevel 1 (
    echo Installing Selenium...
    pip install selenium
) else (
    echo Selenium is already installed.
)

REM Run the tests
echo.
echo Running Selenium tests...
echo.
python tests/selenium_test.py

echo.
echo Tests completed.
pause