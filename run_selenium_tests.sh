#!/bin/bash
# Selenium Test Runner for Dragons & IA
# This script helps run the Selenium tests for the frontend

echo ""
echo "================================================"
echo "   Dragons & IA - Selenium Test Runner"
echo "================================================"
echo ""

# Check if virtual environment exists, if so activate it
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    echo "Activating virtual environment..."
    source venv/Scripts/activate
else
    echo "No virtual environment found. Using system Python."
fi

# Check if selenium is installed, if not install it
if python -c "import selenium" 2>/dev/null; then
    echo "Selenium is already installed."
else
    echo "Installing Selenium..."
    pip install selenium
fi

# Run the tests
echo ""
echo "Running Selenium tests..."
echo ""
python tests/selenium_test.py

echo ""
echo "Tests completed."