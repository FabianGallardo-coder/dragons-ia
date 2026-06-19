#!/bin/bash
# ═══════════════════════════════════════════════
# Dragons & IA — Run all test suites
# ═══════════════════════════════════════════════
set -e

echo "⚔️  Dragons & IA — Running all test suites"
echo "═══════════════════════════════════════════════"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python."
    echo "    Consider running 'scripts/start_local.sh' first to set up the environment."
fi

# Backend tests with pytest
echo ""
echo "🧪 Running backend tests (pytest)..."
echo "────────────────────────────────────────────"
if python -m pytest -v 2>&1; then
    echo "✅ Backend tests passed"
else
    echo "❌ Backend tests failed"
    exit 1
fi

# Frontend logic tests with Node.js
echo ""
echo "🧪 Running frontend logic tests (Node.js)..."
echo "────────────────────────────────────────────"
if node tests/frontend/test_game_logic.js 2>&1; then
    echo "✅ Frontend logic tests passed"
else
    echo "❌ Frontend logic tests failed"
    exit 1
fi

# Selenium tests
echo ""
echo "🧪 Running Selenium end-to-end tests..."
echo "────────────────────────────────────────────"
echo "🔧 Prerequisites: Backend server must be running on http://localhost:8000"
echo "    Start it with: scripts/start_local.sh (in another terminal)"
echo ""
read -p "Press Enter to continue once the backend is running, or Ctrl+C to cancel... " -n1 -s
echo ""
if python tests/selenium_test.py 2>&1; then
    echo "✅ Selenium tests passed"
else
    echo "❌ Selenium tests failed"
    exit 1
fi

echo ""
echo "🎉 All test suites passed!"
echo "═══════════════════════════════════════════════"