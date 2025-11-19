from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

# ================== TRAVELLERS ==================
def open_travellers_dropdown():
    box = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='cars_adults']/ancestor::div[contains(@class,'dropdown-contain')]")
    ))
    box.click()
    time.sleep(0.3)

def get_adults():
    open_travellers_dropdown()
    return int(driver.find_element(By.ID, "cars_adults").get_attribute("value"))

def get_childs():
    return int(driver.find_element(By.ID, "cars_child").get_attribute("value"))

def click_adults_plus(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='qtyInc'])[1]")))
        btn.click()
        time.sleep(0.2)

def click_adults_minus(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='qtyDec'])[1]")))
        btn.click()
        time.sleep(0.2)

def click_childs_plus(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        btn = driver.find_element(By.XPATH, "(//div[@class='qtyInc'])[2]")
        btn.click()
        time.sleep(0.2)

def click_childs_minus(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        btn = driver.find_element(By.XPATH, "(//div[@class='qtyDec'])[2]")
        btn.click()
        time.sleep(0.2)

# ================== TEST CASE TC_29 ==================
def test_TC_29_no_zero_total():
    print("===== TC_29: Không cho tổng Travellers = 0 =====")
    open_travellers_dropdown()

    # Giảm Adults xuống 0
    while get_adults() > 0:
        click_adults_minus(1)
    # Giảm Childs xuống 0
    while get_childs() > 0:
        click_childs_minus(1)

    adults = get_adults()
    childs = get_childs()
    print(f"Adults = {adults}, Childs = {childs}")

    # Nhấn Search
    search_btn = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class,'search_button')]")
    search_btn.click()
    time.sleep(1)

    # Kiểm tra URL hoặc kết quả
    if "cars" in driver.current_url:
        print("❌ FAIL: UI vẫn cho search khi tổng Travellers = 0\n")
    else:
        print("✅ PASS: UI chặn không cho tổng Travellers = 0\n")

# ================== CHẠY TEST ==================
open_homepage()
navigate_to_cars_page()
select_from_airport()
select_to_location()
test_TC_29_no_zero_total()

driver.quit()
