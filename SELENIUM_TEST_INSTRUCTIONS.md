# Instructions for Running Selenium Tests on Dragons & IA Frontend

## Overview
This guide explains how to set up and execute the Selenium test suite for the Dragons & IA frontend. The tests verify that the core user flow pages (homepage, login, register, game) load correctly.

## Prerequisites

### 1. Backend Server Running
Before running the tests, ensure the backend server is running:
```bash
# From the project root directory
docker-compose up -d app
# OR if running directly:
# uvicorn backend.main:app --reload
```
The server should be accessible at http://localhost:8000

### 2. Python Environment
You need Python 3.7+ installed. It's recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Required Packages
Install the Selenium package:
```bash
pip install selenium
```

### 4. ChromeDriver
The tests use Chrome WebDriver in headless mode. You need:
- Google Chrome browser installed
- ChromeDriver matching your Chrome version

**Option A: Let Selenium Manager handle it (Selenium 4.6+)**
Recent Selenium versions can automatically manage drivers:
```bash
pip install selenium  # Version 4.6.0 or higher
```
Selenium will automatically download and manage the appropriate ChromeDriver.

**Option B: Manual ChromeDriver installation**
1. Download ChromeDriver from: https://chromedriver.chromium.org/downloads
2. Ensure it matches your Chrome browser version
3. Add the ChromeDriver executable to your system PATH
   - Or place it in the same directory as your test script

## Running the Tests

### From Project Root Directory
```bash
# Ensure backend is running (http://localhost:8000)
# Activate your virtual environment if using one
python tests/selenium_test.py
```

### Expected Output
```
Starting Selenium tests for Dragons & IA...
✓ Homepage loads correctly
✓ Login page loads correctly
✓ Register page loads correctly
✓ Game page accessible

✅ All tests passed!
```

## Test Details

### What the Tests Verify
1. **Homepage Loads**: Checks that the root URL loads and contains "Dragons & IA" in the title
2. **Login Page Loads**: Verifies `/login.html` loads and contains login-related text
3. **Register Page Loads**: Verifies `/register.html` loads and contains registration-related text
4. **Game Page Accessible**: Checks that `/game.html` loads (may redirect to login if not authenticated)

### Test Configuration
- **Base URL**: `http://localhost:8000` (modify `BASE_URL` in the script if needed)
- **Wait Time**: 10 seconds explicit waits for elements
- **Browser**: Headless Chrome (no UI visible during testing)
- **Timeout**: Each test waits up to 10 seconds for elements to appear

## Troubleshooting

### Common Issues

**1. "WebDriverException: Message: 'chromedriver' executable needs to be in PATH"**
   - Solution: Install ChromeDriver and add it to PATH, or use Selenium 4.6+ with automatic driver management

**2. "SessionNotCreatedException: This version of ChromeDriver only supports Chrome version XX"**
   - Solution: Update ChromeDriver to match your Chrome browser version, or update Chrome to match the driver

**3. "Connection refused" or timeout errors**
   - Solution: Ensure the backend server is running and accessible at http://localhost:8000
   - Check with: `curl http://localhost:8000/health` should return 200 OK

**4. Element not found / timeout exceptions**
   - Solution: The frontend may have changed. Verify the expected text in the HTML files:
     - Login page: Should contain "Iniciar sesión" or "Login"
     - Register page: Should contain "Registro" or "Register"

**5. Permission issues with ChromeDriver**
   - On Linux/Mac: Make ChromeDriver executable: `chmod +x chromedriver`
   - On Windows: Ensure you have permission to execute the file

## Alternative: Using Firefox
If you prefer Firefox, modify the `setup_driver()` function:
```python
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def setup_driver():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    # GeckoDriver will be managed automatically with Selenium 4.6+
    # Or ensure geckodriver is in PATH
    driver = webdriver.Firefox(options=firefox_options)
    return driver
```
And install: `pip install selenium` (same package works for both)

## Integration with Existing Test Suite
The project already has:
- Backend tests: Run with `pytest -v` (see `pytest.ini` configuration)
- Frontend logic tests: Node.js tests in `tests/frontend/`

These Selenium tests complement the existing test suite by providing end-to-end browser-based validation of the user interface.

## Notes
- Tests run in headless mode by default - no browser window will be visible
- To see the browser during testing, remove the `--headless` argument from `setup_driver()`
- The test script is designed to be run independently; it's not integrated into the main pytest suite
- For CI/CD pipelines, you can add this script to your test stage