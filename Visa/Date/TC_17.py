from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# ================== CONFIG ==================
HOME_URL = "https://www.phptravels.net"
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)
DATE_INPUT_XPATH = "//input[@id='date']"

# ================== COMMON ==================
def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def navigate_to_visa_page():
    visa_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/visa')]")))
    visa_link.click()
    wait.until(EC.url_contains("visa"))

def open_calendar():
    """Click vào ô Date để mở calendar"""
    date_input = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_INPUT_XPATH)))
    date_input.click()
    print("📌 Calendar mở ra.")

# ================== TEST CALENDAR ==================
def test_calendar_actions():
    open_calendar()
    time.sleep(0.5)

    # 1. Click icon Next Month
    next_btn = driver.find_element(By.CLASS_NAME, "next")
    next_btn.click()
    print("➡️ Click Next Month")
    time.sleep(0.5)

    # 2. Click icon Previous Month
    prev_btn = driver.find_element(By.CLASS_NAME, "prev")
    prev_btn.click()
    print("⬅️ Click Prev Month")
    time.sleep(0.5)

    # 3. Click dropdown Month-Year
    switch_btn = driver.find_element(By.CLASS_NAME, "switch")
    switch_btn.click()
    print("📅 Mở dropdown tháng-năm")
    time.sleep(0.5)

    # 4. Lấy danh sách tất cả ngày trong tháng hiện tại
    day_elements = driver.find_elements(By.XPATH, "//td[contains(@class,'day') and not(contains(@class,'old'))]")
    print(f"📆 Số ngày có thể chọn trong tháng: {len(day_elements)}")

    # 5. Chọn ngẫu nhiên 1 ngày
    chosen_day = random.choice(day_elements)
    day_text = chosen_day.text.strip()
    chosen_day.click()
    time.sleep(0.5)

    # 6. Kiểm tra giá trị hiển thị trong input Date
    displayed_value = driver.find_element(By.XPATH, DATE_INPUT_XPATH).get_attribute("value")
    print(f"🧩 Ngày hiển thị trong textbox: {displayed_value}")
    print(f"✅ Ngày đã chọn: {day_text}")

# ================== RUN ==================
open_homepage()
navigate_to_visa_page()
test_calendar_actions()

driver.quit()
