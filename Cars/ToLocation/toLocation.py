from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

import time

# ===================== CẤU HÌNH CHUNG =====================
HOME_URL = "https://www.phptravels.net"
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ===================== HÀM CHUNG =====================
def open_homepage():
    print("Truy cập trang chủ PHPTravels...")
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Đã mở trang chủ.\n")

def navigate_to_cars_page():
    print("Chuyển sang trang Cars...")
    cars_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/cars')]")
    ))
    cars_link.click()
    wait.until(EC.url_contains("cars"))
    print(f"✅ Đã vào trang Cars: {driver.current_url}\n")

def open_to_location_dropdown():
    """Mở dropdown To Location và trả về ô input để nhập dữ liệu"""
    print("Mở dropdown 'To Location'...")
    # Click vào dropdown To Location
    to_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='input-items cars_location']//span[@role='combobox']")
    ))
    to_dropdown.click()
    # Lấy ô input ẩn bên trong dropdown
    search_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(@class,'select2-dropdown--below')]//input[@class='select2-search__field']")
    ))
    return search_box

# ===================== TEST CASES =====================
def test_TC_10_valid_input():
    """TC_10: Nhập >=3 ký tự hợp lệ"""
    search_box = open_to_location_dropdown()
    search_box.clear()
    search_box.send_keys("Lon")  # >=3 ký tự hợp lệ
    time.sleep(1)
    results = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//span[contains(@class,'select2-dropdown--below')]//li[contains(@class,'select2-results__option')]")
    ))
    if len(results) > 0:
        print(f"✅ TC_10 PASSED: Hiển thị {len(results)} gợi ý\n")
    else:
        print("❌ TC_10 FAILED: Không hiển thị gợi ý\n")

def test_TC_11_short_input():
    """TC_11: Nhập < 3 ký tự"""
    print("➡️ TC_11: Nhập <3 ký tự...")
    # đảm bảo dropdown trước đã đóng
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(0.5)

    to_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='input-items cars_location']//span[@role='combobox']")
    ))
    to_dropdown.click()

    search_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@class='select2-search__field']")
    ))
    search_box.clear()
    search_box.send_keys("L")
    time.sleep(1)

    try:
        msg = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//li[contains(@class,'select2-results__message') and contains(text(),'Please enter')]")
        ))
        print(f"✅ TC_11 PASSED: Hiển thị thông báo '{msg.text}'")
    except:
        print("❌ TC_11 FAILED: Không thấy thông báo")


def test_TC_12_no_results_found():
    """[TC12] Nhập ký tự đặc biệt hoặc từ không tồn tại → Hiển thị 'No results found'"""
    print("\n🔍 [TC12] Kiểm tra nhập dữ liệu không tồn tại hoặc ký tự đặc biệt...")

    # 1️⃣ Nếu dropdown cũ đang mở, lấy thẳng input hiện tại
    try:
        search_box = driver.find_element(By.XPATH, "//input[@class='select2-search__field']")
    except:
        # Nếu chưa mở, click mở dropdown
        to_dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@class='input-items cars_location']//span[@role='combobox']"
        )))
        to_dropdown.click()
        search_box = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//input[@class='select2-search__field']"
        )))

    # 2️⃣ Danh sách dữ liệu kiểm tra
    test_inputs = ["@@@", "qwertyuiop", "randomcity123"]

    for test_input in test_inputs:
        print(f"\n➡ Nhập thử: '{test_input}'")
        search_box.clear()
        search_box.send_keys(test_input)
        time.sleep(2)

        try:
            message_element = wait.until(EC.presence_of_element_located((
                By.XPATH, "//li[contains(@class,'select2-results__message') and normalize-space()='No results found']"
            )))
            print(f"✅ PASSED: '{test_input}' → Hiển thị thông báo: '{message_element.text}'")
        except:
            print(f"⚠ FAILED: '{test_input}' → Không hiển thị thông báo 'No results found'")

    # 3️⃣ Thoát dropdown sau khi test xong
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(1)

def test_TC_13_select_random_suggestion():
    """[TC13] Nhập và chọn gợi ý bất kỳ → kiểm tra giá trị hiển thị trên ô To Location"""
    print("\n🔍 [TC13] Nhập và chọn gợi ý ngẫu nhiên...")

    # 1️⃣ Mở dropdown To Location (hoặc lấy thẳng input nếu đã mở)
    try:
        search_box = driver.find_element(By.XPATH, "//input[@class='select2-search__field']")
    except:
        to_dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@class='input-items cars_location']//span[@role='combobox']"
        )))
        to_dropdown.click()
        search_box = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//input[@class='select2-search__field']"
        )))

    # 2️⃣ Nhập dữ liệu vào ô input
    test_input = "Lon"  # bạn có thể đổi từ khác
    print(f"Nhập '{test_input}' vào To Location...")
    search_box.clear()
    search_box.send_keys(test_input)
    time.sleep(2)

    # 3️⃣ Lấy tất cả gợi ý hiện ra
    suggestions = wait.until(EC.presence_of_all_elements_located((
        By.XPATH, "//ul[contains(@class,'select2-results__options')]/li[not(contains(@class,'select2-results__message'))]"
    )))

    if not suggestions:
        print("❌ FAILED: Không có gợi ý nào xuất hiện")
        return

    # 4️⃣ Chọn một gợi ý ngẫu nhiên
    random_suggestion = random.choice(suggestions)
    selected_text = random_suggestion.text.strip()
    print(f"Chọn gợi ý ngẫu nhiên: '{selected_text}'")
    random_suggestion.click()
    time.sleep(1)

    # 5️⃣ Kiểm tra giá trị hiển thị trên ô To Location
    selected_value = driver.find_element(
        By.XPATH,
        "//div[@class='input-items cars_location']//span[@role='combobox']/span[@class='select2-selection__rendered']"
    ).text.strip()

    # Tách tên thành phố từ gợi ý (bỏ phần sau dấu phẩy nếu có)
    city_name = selected_text.split(",")[0].strip()

    # So sánh tên thành phố
    if city_name.lower() in selected_value.lower():
        print(f"✅ PASSED: Giá trị hiển thị '{selected_value}' chứa tên thành phố '{city_name}'")
    else:
        print(f"❌ FAILED: Giá trị hiển thị '{selected_value}' không chứa tên thành phố '{city_name}'")




# ===================== RUN ALL TESTS =====================
try:
    open_homepage()
    navigate_to_cars_page()
    test_TC_10_valid_input()
    test_TC_11_short_input()
    test_TC_12_no_results_found()
    test_TC_13_select_random_suggestion()
finally:
    print("Đóng trình duyệt...")
    driver.quit()
