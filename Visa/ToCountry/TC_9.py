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
    # Chọn đúng dropdown To Country (dropdown thứ 2 trên page)
    dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//span[@role='combobox'])[2]")
    ))
    dropdown.click()
    time.sleep(1)
    return dropdown

def get_dropdown_items():
    """Lấy tất cả item trong dropdown đang mở"""
    return driver.find_elements(By.XPATH, "//ul[contains(@id,'results')]/li")

# ================== TEST CASE ==================

# TC_3 – Kiểm tra hiển thị danh sách To Country
def test_tc3_check_to_country_values():
    print("🔎 TC_3: Kiểm tra hiển thị dữ liệu trong To Country droplist...")
    open_to_country_dropdown()

    items = get_dropdown_items()
    print(f"👉 Số lượng quốc gia tìm thấy: {len(items)}")

    assert len(items) > 0, "❌ Không có dữ liệu trong dropdown!"
    print("➡️ 5 giá trị đầu tiên:")
    for item in items[:5]:
        print(" -", item.text)

    print("✅ TC_3 Passed.\n")


# ================== RUN ==================
open_homepage()
navigate_to_visa_page()

test_tc3_check_to_country_values()

driver.quit()
