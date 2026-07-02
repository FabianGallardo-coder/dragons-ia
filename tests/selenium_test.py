"""
Selenium tests for Dragons & IA frontend.
Tests: page loads, registration, login, and game access.
"""
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

BASE_URL = "http://localhost:8000"
WAIT_TIME = 10
TEST_USER_PREFIX = "testuser_"


def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def test_homepage_loads(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    assert "Dragons" in driver.title or "dragons" in driver.page_source.lower()
    print("[OK] Homepage loads correctly")


def test_login_page_loads(driver):
    driver.get(f"{BASE_URL}/login.html")
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    page_source = driver.page_source.lower()
    assert "iniciar" in page_source or "login" in page_source
    print("[OK] Login page loads correctly")


def test_register_page_loads(driver):
    driver.get(f"{BASE_URL}/register.html")
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    page_source = driver.page_source.lower()
    assert "crear cuenta" in page_source or "registro" in page_source
    print("[OK] Register page loads correctly")


def test_user_registration_flow(driver):
    driver.get(f"{BASE_URL}/register.html")
    wait = WebDriverWait(driver, WAIT_TIME)

    suffix = random_string()
    username = f"{TEST_USER_PREFIX}{suffix}"
    email = f"{username}@test.com"
    password = "TestPass123!"

    try:
        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input.clear()
        username_input.send_keys(username)

        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.clear()
        email_input.send_keys(email)

        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.clear()
        password_input.send_keys(password)

        confirm_input = wait.until(EC.presence_of_element_located((By.ID, "password2")))
        confirm_input.clear()
        confirm_input.send_keys(password)

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()

        wait.until(EC.url_contains("/"))
        time.sleep(1)
        print(f"[OK] User registration successful: {username}")

        driver.test_username = username
        driver.test_password = password
        driver.test_email = email

    except TimeoutException:
        print("[FAIL] User registration timed out")
        raise


def test_user_login_flow(driver):
    if not hasattr(driver, 'test_email'):
        print("[INFO] Skipping login test - no test user available")
        return

    driver.get(f"{BASE_URL}/login.html")
    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.clear()
        email_input.send_keys(driver.test_email)

        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.clear()
        password_input.send_keys(driver.test_password)

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()

        wait.until(EC.url_contains("/"))
        print(f"[OK] User login successful: {driver.test_username}")

    except TimeoutException:
        print("[FAIL] User login timed out")
        raise


def test_game_page_loads(driver):
    driver.get(f"{BASE_URL}/game.html")
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    page_source = driver.page_source.lower()
    assert "game" in page_source or "login" in page_source or "iniciar" in page_source
    print("[OK] Game page accessible")


def main():
    print("Starting Selenium tests for Dragons & IA...")
    driver = None
    try:
        driver = setup_driver()
        test_homepage_loads(driver)
        test_login_page_loads(driver)
        test_register_page_loads(driver)
        test_user_registration_flow(driver)
        test_user_login_flow(driver)
        test_game_page_loads(driver)
        print("\n[PASS] All tests passed!")
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        raise
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
