from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

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
def check_today_in_date_input():
    """Kiểm tra giá trị trong ô Date có phải là ngày hôm nay không"""
    date_input = wait.until(EC.presence_of_element_located((By.XPATH, DATE_INPUT_XPATH)))
    date_value = date_input.get_attribute("value")  # ví dụ: "04-12-2025"

    today = datetime.datetime.now()
    today_str = today.strftime("%d-%m-%Y")  # format dd-mm-yyyy

    if date_value == today_str:
        print(f"✅ Giá trị trong ô Date '{date_value}' là ngày hôm nay.")
    else:
        print(f"❌ Giá trị trong ô Date '{date_value}' KHÔNG phải ngày hôm nay ({today_str}).")

# ================== RUN ==================
open_homepage()
navigate_to_visa_page()
check_today_in_date_input()

driver.quit()
