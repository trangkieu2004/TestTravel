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

def login():
    print("🔑 Đăng nhập vào tài khoản...")
    driver.get(f"{HOME_URL}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "submitBTN").click()
    wait.until(EC.url_contains("dashboard"))
    print("✅ Login thành công!\n")

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

def TC_33_validate_user_info_displayed():
    print("🧾 TC_33: Kiểm tra hiển thị đầy đủ các trường & tự động điền thông tin khi đã đăng nhập...")

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)

    # Danh sách các trường cần có
    required_fields = {
        "First Name": "//input[@id='p-first-name']",
        "Last Name": "//input[@id='p-last-name']",
        "Email": "//input[@id='p-email']",
        "Phone": "//input[@id='p-phone']",
        "Address": "//input[@id='p-address']",
        "Nationality": "//div[@class='filter-option']",
        "Current Country": "//select[@name='country']"
    }

    # 1️⃣ Kiểm tra tất cả các field có tồn tại trên trang
    for label, xpath in required_fields.items():
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            print(f"✅ Field tồn tại: {label}")
        except:
            print(f"❌ Field KHÔNG tồn tại: {label}")

    # 2️⃣ Kiểm tra thông tin đã được tự động điền đúng
    print("\n🔍 Kiểm tra nội dung auto-filled...")

    first_name = driver.find_element(By.NAME, "first_name").get_attribute("value")
    last_name = driver.find_element(By.NAME, "last_name").get_attribute("value")
    email = driver.find_element(By.NAME, "email").get_attribute("value")
    phone = driver.find_element(By.NAME, "phone").get_attribute("value")

    # Email phải khớp với tài khoản login
    if email == EMAIL:
        print(f"✅ Email tự động điền đúng: {email}")
    else:
        print(f"❌ Email sai! Giá trị: {email}")

    # Các giá trị khác chỉ kiểm tra KHÔNG rỗng (do mỗi account khác nhau)
    if first_name.strip():
        print(f"✅ First Name tự động điền: {first_name}")
    else:
        print("❌ First Name bị trống!")

    if last_name.strip():
        print(f"✅ Last Name tự động điền: {last_name}")
    else:
        print("❌ Last Name bị trống!")

    if phone.strip():
        print(f"✅ Phone tự động điền: {phone}")
    else:
        print("❌ Phone bị trống!")

    print("\n🎉 TC_33 Completed.\n")


# ================== CHẠY FLOW ==================
open_homepage()
login()
navigate_to_cars_page()
select_from_airport()
select_to_location()
set_travellers(adults=1, childs=1)
search_and_book()
TC_33_validate_user_info_displayed()

driver.quit()
