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

def navigate_to_visa_page():
    print("➡️ Điều hướng sang trang Visa...")
    visa_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/visa')]")))
    visa_link.click()
    wait.until(EC.url_contains("visa"))
    print("✅ Đã vào trang Visa.\n")

# ================== HỖ TRỢ DROPDOWN ==================
def open_to_country_dropdown():
    print("\n📌 Mở dropdown To Country...")
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@role='combobox'])[2]")))
    dropdown.click()
    time.sleep(1)
    # Lấy ô search input bên trong dropdown
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='select2-search__field']")))
    return search_box

def get_dropdown_items():
    """Lấy tất cả item trong dropdown đang mở"""
    return driver.find_elements(By.XPATH, "//ul[contains(@id,'results')]/li")

# ================== TEST CASE ==================

# TC_XX – Kiểm tra dropdown khi nhập toàn space hoặc không nhập
def test_to_country_no_input_or_space():
    print("🔎 TC_XX: Kiểm tra To Country khi nhập trống hoặc toàn space")
    
    search_box = open_to_country_dropdown()
    
    # --- Không nhập gì ---
    search_box.clear()
    time.sleep(1)
    items_empty = get_dropdown_items()
    print(f"👉 Không nhập gì - số lượng item: {len(items_empty)}")

    # --- Nhập toàn space ---
    search_box.clear()
    search_box.send_keys("   ")  # 3 space
    time.sleep(1)
    items_space = get_dropdown_items()
    print(f"👉 Nhập toàn space - số lượng item: {len(items_space)}")
    
    # Kiểm tra
    if len(items_empty) > 0 and len(items_space) > 0:
        print("✅ PASSED: Khi không nhập hoặc nhập toàn space, hiển thị tất cả quốc gia.")
    else:
        print("❌ FAILED: Không hiển thị danh sách quốc gia đầy đủ.")


# ================== RUN ==================
open_homepage()
navigate_to_visa_page()

test_to_country_no_input_or_space()

driver.quit()
