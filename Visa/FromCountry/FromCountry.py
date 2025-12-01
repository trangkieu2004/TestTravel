from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.common.keys import Keys
import time

# ================== CONFIG ==================
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

HOME_URL = "https://www.phptravels.net"

# ================== COMMON ==================
def open_homepage():
    print("🌍 Mở trang chủ...")
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Trang chủ đã mở.\n")

def go_to_visa_page():
    print("✈️ Chuyển sang trang Visa...")
    visa_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'/visa')]")
    ))
    visa_link.click()
    wait.until(EC.url_contains("visa"))
    print("✅ Đã vào trang Visa.\n")

# ================== FUNCTION ==================
def open_from_country_dropdown():
    """Mở dropdown Select2 của From Country"""
    print("\n📌 Mở dropdown 'From Country'...")

    # Xác định combobox select2
    dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@id='select2--container']/ancestor::span[@role='combobox']")
    ))

    dropdown.click()

    # Trả về ô search field
    return wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@class='select2-search__field']")
    ))

# ================== TEST CASE 1 ==================
def test_tc01_valid_search(search_box):
    """Nhập >=3 ký tự → phải có kết quả"""
    test_input = "Vi"
    print(f"\n🔍 [TC01] Tìm kiếm hợp lệ với '{test_input}'...")

    search_box.send_keys(test_input)
    time.sleep(2)

    items = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//ul[@id='select2--results']//li[contains(@class,'select2-results__option')]")
    ))

    if len(items) > 0:
        print(f"✅ PASSED: Có {len(items)} kết quả khi nhập '{test_input}'")
    else:
        print(f"❌ FAILED: Không tìm thấy kết quả!")

    return items

# ================== TEST CASE 2 ==================
def test_tc02_invalid_search(search_box):
    """Nhập không hợp lệ → trả về No Results"""
    test_input = "xxxxx"
    print(f"\n🔍 [TC02] Tìm kiếm không hợp lệ với '{test_input}'...")

    search_box.clear()
    search_box.send_keys(test_input)
    time.sleep(1)

    try:
        no_result = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class,'select2-results__message') and contains(text(),'No results found')]")
))

        print("✅ PASSED: Không có kết quả khi nhập từ khóa sai")
    except:
        print("❌ FAILED: Hệ thống vẫn trả ra kết quả!")

# ================== RUN ==================
open_homepage()
go_to_visa_page()

# Mở dropdown From Country
search_box = open_from_country_dropdown()

test_tc01_valid_search(search_box)
test_tc02_invalid_search(search_box)

# ================== QUIT ==================
driver.quit()