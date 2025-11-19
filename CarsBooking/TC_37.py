from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ================== CẤU HÌNH ==================
HOME_URL = "https://www.phptravels.net"
EMAIL = "user@phptravels.com"
PASSWORD = "demouser"

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

# ================== CHỌN TRAVELLERS ==================
def set_travellers(adults=1, childs=1):
    print(f"👨‍👩‍👧 Set Travellers: Adults={adults}, Childs={childs}")
    dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='cars_adults']/ancestor::div[contains(@class,'dropdown-contain')]")
    ))
    dropdown.click()
    time.sleep(0.3)

    # Adults
    adults_input = driver.find_element(By.ID, "cars_adults")
    current_adults = int(adults_input.get_attribute("value"))
    plus_btn = driver.find_element(By.XPATH, "(//div[@class='qtyInc'])[1]")
    minus_btn = driver.find_element(By.XPATH, "(//div[@class='qtyDec'])[1]")

    while current_adults < adults:
        plus_btn.click()
        current_adults += 1
        time.sleep(0.2)
    while current_adults > adults:
        minus_btn.click()
        current_adults -= 1
        time.sleep(0.2)

    # Childs
    childs_input = driver.find_element(By.ID, "cars_child")
    current_childs = int(childs_input.get_attribute("value"))
    plus_btn_c = driver.find_element(By.XPATH, "(//div[@class='qtyInc'])[2]")
    minus_btn_c = driver.find_element(By.XPATH, "(//div[@class='qtyDec'])[2]")

    while current_childs < childs:
        plus_btn_c.click()
        current_childs += 1
        time.sleep(0.2)
    while current_childs > childs:
        minus_btn_c.click()
        current_childs -= 1
        time.sleep(0.2)

    # Đóng dropdown
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(0.3)
    print("✅ Travellers set xong.\n")

# ================== TÌM XE & BOOK ==================
def search_and_book():
    print("🔍 Nhấn Search...")
    search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class,'search_button')]")))
    search_btn.click()
    time.sleep(2)

    print("🚘 Nhấn Book Now xe đầu tiên...")
    first_book = wait.until(EC.element_to_be_clickable((
        By.XPATH, "(//button[contains(text(),'Book Now')])[1]"
    )))
    first_book.click()

    # Kiểm tra có vào trang Cars Booking không
    try:
        wait.until(EC.url_contains("cars/booking"))
        print("✅ PASS: Chuyển đến trang Cars Booking.\n")
    except:
        print("❌ FAIL: Không vào trang Cars Booking.\n")

# ================== FORM BOOKING – HỖ TRỢ ==================
def fill_booking_form_all_empty_and_submit():
    """Điền trống tất cả field và click BOOKING để trigger validate"""
    
    # Clear tất cả field và click để focus
    fields = [
        "//input[@id='p-first-name']",
        "//input[@id='p-last-name']",
        "//input[@id='p-email']",
        "//input[@id='p-phone']",
        "//input[@id='p-address']"
    ]
    for xpath in fields:
        f = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        f.clear()
        f.click()
        time.sleep(0.1)

    # Tick checkbox
    checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='form-check-input']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    checkbox.click()
    time.sleep(0.3)

    # Click BOOKING để trigger error
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='booking']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    btn.click()
    time.sleep(1)  # đợi JS render error messages

def TC_37_validate_valid_email():
    print("=== TC_37: Validate Email hợp lệ ===")

    # Điền form với tất cả field hợp lệ
    first_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='p-first-name']")))
    first_input.clear(); first_input.send_keys("John")

    last_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='p-last-name']")))
    last_input.clear(); last_input.send_keys("Tester")

    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='p-email']")))
    email_input.clear(); email_input.send_keys("abc@gmail.com")  # ✅ hợp lệ

    phone_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='p-phone']")))
    phone_input.clear(); phone_input.send_keys("0123456789")

    addr_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='p-address']")))
    addr_input.clear(); addr_input.send_keys("Hanoi")

    # Tick checkbox
    checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='form-check-input']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(0.5)

    # Click BOOKING bằng JS
    btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='booking']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)

    # Kiểm tra không có lỗi nào hiển thị
    error_elements = driver.find_elements(By.XPATH, "//div[contains(@id,'-error')]")
    errors_text = [e.text.strip() for e in error_elements if e.text.strip()]

    if len(errors_text) == 0:
        print("✅ PASS TC_37 – Tất cả field hợp lệ, không có message lỗi!")
    else:
        print("❌ FAIL TC_37 – Vẫn còn lỗi:", errors_text)

open_homepage()
navigate_to_cars_page()
select_from_airport()
select_to_location()
set_travellers(adults=1, childs=1)
search_and_book()
TC_37_validate_valid_email()

driver.quit()
