from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# ================== CONFIG ==================
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)
HOME_URL = "https://www.phptravels.net"
DATE_INPUT_XPATH = "//input[@id='date']"

# ================== COMMON ==================
def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def navigate_to_visa_page():
    visa_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/visa')]")))
    visa_link.click()
    wait.until(EC.url_contains("visa"))

def open_datepicker():
    date_input = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_INPUT_XPATH)))
    date_input.click()
    calendar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "datepicker-days")))
    return calendar

# ================== TEST: KHÔNG CHỌN ĐƯỢC NGÀY QUÁ KHỨ ==================
def test_select_past_date_via_prev():
    """Test ngày quá khứ bằng cách click prev month"""
    open_datepicker()

    # Click nút Previous Month
    prev_btn = driver.find_element(By.CLASS_NAME, "prev")
    prev_btn.click()
    print("⬅️ Đã click Previous Month")

    # Chờ calendar load xong
    time.sleep(0.5)

    # Lấy lại các ngày sau khi DOM thay đổi
    past_days = driver.find_elements(By.XPATH, "//td[contains(@class,'old') or contains(@class,'day')]")

    if not past_days:
        print("⚠️ Không tìm thấy ngày trong tháng trước")
        return

    for day in past_days:
        try:
            # Thử click, nếu không click được sẽ ném lỗi
            day.click()
            print("❌ Ngày quá khứ có thể click được! (Sai behavior)")
        except Exception:
            # Lấy lại text của element trước khi DOM thay đổi
            day_text = day.get_attribute("textContent")  # dùng get_attribute thay vì .text
            print(f"✅ Không thể click vào ngày quá khứ: {day_text}")


# ================== RUN ==================
open_homepage()
navigate_to_visa_page()
test_select_past_date_via_prev()
driver.quit()
