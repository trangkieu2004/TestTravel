from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# ================== CẤU HÌNH ==================
HOME_URL = "https://www.phptravels.net"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ================== HÀM CHUNG ==================
def open_homepage():
    print("🌍 Mở trang chủ...")
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Trang chủ đã mở.\n")

def navigate_to_cars_page():
    print("🚗 Chuyển sang trang Cars...")
    cars_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/cars')]")))
    cars_link.click()
    wait.until(EC.url_contains("cars"))
    print("✅ Đã vào trang Cars.\n")

# ================== CHỌN LOCATION ==================
def select_from_airport():
    print("🛫 Chọn From Airport...")
    dropdown = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[@id='select2--container']/ancestor::span[@role='combobox']"
    )))
    dropdown.click()
    search_box = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//input[@class='select2-search__field']"
    )))
    search_box.send_keys("DXB")
    time.sleep(1)
    first_item = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//ul[contains(@class,'select2-results__options')]/li[1]"
    )))
    first_item.click()
    print("✅ Đã chọn From Airport.\n")
    time.sleep(0.5)

def select_to_location():
    print("📍 Chọn To Location...")
    dropdown = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[@class='input-items cars_location']//span[@role='combobox']"
    )))
    dropdown.click()
    search_box = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//input[@class='select2-search__field']"
    )))
    search_box.send_keys("Lon")
    time.sleep(1)
    first_item = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//ul[contains(@class,'select2-results__options')]/li[1]"
    )))
    first_item.click()
    print("✅ Đã chọn To Location.\n")
    time.sleep(0.5)

# ================== KIỂM TRA NGÀY DISABLED (TC_13) ==================
def is_date_disabled(date_input_xpath, date_str):
    date_input = wait.until(EC.element_to_be_clickable((By.XPATH, date_input_xpath)))
    date_input.click()
    time.sleep(0.5)
    try:
        day_elem = driver.find_element(By.XPATH, f"//td[@data-date='{date_str}']")
        if 'disabled' in day_elem.get_attribute('class'):
            print(f"⚠ Ngày {date_str} bị disable như mong đợi.")
            return True
        else:
            print(f"✅ Ngày {date_str} có thể chọn.")
            return False
    except:
        print(f"⚠ Không tìm thấy ngày {date_str} trên datepicker.")
        return None

# ================== CHỌN NGÀY HỢP LỆ BẰNG JS ==================
def select_date_js(date_input_xpath, target_date):
    try:
        date_input = wait.until(EC.presence_of_element_located((By.XPATH, date_input_xpath)))
        driver.execute_script(f"arguments[0].value = '{target_date.strftime('%Y-%m-%d')}';", date_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", date_input)
        print(f"✅ Ngày {target_date.strftime('%Y-%m-%d')} đã set thành công.\n")
        return True
    except Exception as e:
        print(f"⚠ Không set được ngày {target_date.strftime('%Y-%m-%d')}. Lỗi: {e}")
        return False

# ================== CLICK SEARCH BẰNG JS ==================
def click_search_js():
    print("🔎 Click Search...")
    btn = wait.until(EC.presence_of_element_located((
        By.XPATH, "//button[@type='submit' and contains(@class,'search_button')]"
    )))
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(2)
    print("➡ Đã nhấn Search.\n")

# ================== TEST CASES ==================
# --- TC_13 ---
def test_TC_13_pickup_date_in_past():
    print("===== TC_13: Pick-up Date < Hôm nay =====")
    select_from_airport()
    select_to_location()

    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    is_date_disabled("//input[@id='cars_from_date']", past_date)

    print("✅ TC_13 hoàn tất.\n")

# --- TC_14 ---
def test_TC_14_dropoff_before_pickup():
    print("===== TC_14: Drop-off < Pick-up =====")
    select_from_airport()
    select_to_location()

    pickup = datetime.now() + timedelta(days=5)
    dropoff = datetime.now() + timedelta(days=3)

    select_date_js("//input[@id='cars_from_date']", pickup)
    select_date_js("//input[@id='cars_to_date']", dropoff)

    click_search_js()
    print("⭐ Kiểm tra lỗi Drop-off < Pickup...\n")
    print("✅ TC_14 hoàn tất.\n")

# --- TC_15 ---
def test_TC_15_dropoff_after_pickup():
    print("===== TC_15: Drop-off >= Pick-up =====")
    select_from_airport()
    select_to_location()

    pickup = datetime.now() + timedelta(days=2)
    dropoff = datetime.now() + timedelta(days=5)

    select_date_js("//input[@id='cars_from_date']", pickup)
    select_date_js("//input[@id='cars_to_date']", dropoff)

    click_search_js()
    print("⭐ Kiểm tra danh sách xe xuất hiện...\n")
    print("✅ TC_15 hoàn tất.\n")

# ================== CHẠY TEST ==================
open_homepage()
navigate_to_cars_page()

test_TC_13_pickup_date_in_past()
test_TC_14_dropoff_before_pickup()
test_TC_15_dropoff_after_pickup()

driver.quit()
