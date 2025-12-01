from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import random
import time

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

# ================== FUNCTION ==================
def open_calendar():
    """Click vào ô Date để mở calendar"""
    date_input = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_INPUT_XPATH)))
    date_input.click()
    print("📌 Calendar mở ra.")

def select_future_date():
    """Chọn 1 ngày bất kỳ trong tương lai và kiểm tra hiển thị"""
    today = datetime.datetime.now()
    # Lấy danh sách các ngày trong calendar có class 'day' và không phải 'old day' (quá khứ)
    future_days = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//td[contains(@class,'day') and not(contains(@class,'old'))]")
    ))

    # Chọn 1 ngày bất kỳ trong tương lai
    chosen_day_elem = random.choice(future_days)
    chosen_day_text = chosen_day_elem.text.strip()
    chosen_date = today.replace(day=int(chosen_day_text))  # giữ tháng/năm hiện tại
    chosen_day_elem.click()
    time.sleep(1)

    # Lấy giá trị hiển thị trong input Date
    displayed_value = driver.find_element(By.XPATH, DATE_INPUT_XPATH).get_attribute("value")
    displayed_date = datetime.datetime.strptime(displayed_value, "%d-%m-%Y")

    print(f"🌟 Chọn ngày: {chosen_day_text} tháng {today.month} năm {today.year}")
    print(f"🧩 Giá trị hiển thị trong textbox: {displayed_value}")

    if displayed_date.day == int(chosen_day_text) and displayed_date.month == today.month and displayed_date.year == today.year:
        print("✅ Ngày hiển thị đúng với ngày đã chọn.")
    else:
        print("❌ Ngày hiển thị KHÔNG đúng với ngày đã chọn.")

# ================== RUN ==================
open_homepage()
navigate_to_visa_page()
open_calendar()
select_future_date()

driver.quit()
