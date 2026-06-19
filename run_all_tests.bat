@echo off
REM ══════════════════════════════════════════════
REM Dragons & IA — Run all test suites
REM ══════════════════════════════════════════════

echo.
echo ⚔️  Dragons ^& IA — Running all test suites
echo ══════════════════════════════════════════════

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Using system Python.
    echo     Consider running scripts\start_local.bat first to set up the environment.
)

REM Backend tests with pytest
echo.
echo 🧪 Running backend tests (pytest)...
echo ────────────────────────────────────────────
python -m pytest -v
if errorlevel 1 (
    echo ❌ Backend tests failed
    exit /b 1
) else (
    echo ✅ Backend tests passed
)

REM Frontend logic tests with Node.js
echo.
echo 🧪 Running frontend logic tests (Node.js)...
echo ────────────────────────────────────────────
node tests/frontend/test_game_logic.js
if errorlevel 1 (
    echo ❌ Frontend logic tests failed
    exit /b 1
) else (
    echo ✅ Frontend logic tests passed
)

REM Selenium tests
echo.
echo 🧪 Running Selenium end-to-end tests...
echo ────────────────────────────────────────────
echo 🔧 Prerequisites: Backend server must be running on http://localhost:8000
echo    Start it with: scripts\start_local.bat (in another terminal)
echo.
set /p "=Press Enter to continue once the backend is running, or Ctrl+C to cancel... "
echo.
python tests/selenium_test.py
if errorlevel 1 (
    echo ❌ Selenium tests failed
    exit /b 1
) else (
    echo ✅ Selenium tests passed
)

echo.
echo 🎉 All test suites passed!
echo ═════════════════════════════════════════════