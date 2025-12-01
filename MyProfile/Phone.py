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

def navigate_to_profile_page():
    print("🚗 Chuyển sang trang My Profile...")
    cars_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='My Profile']]")))
    cars_link.click()
    wait.until(EC.url_contains("profile"))
    print("✅ Đã vào trang Profile.\n")

# ===== Hàm dùng chung =======
def click_update_profile():
    update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Update Profile')]")))
    update_btn.click()
    time.sleep(1)  # cho UI load popup nhanh

def fill_required_password():
    pwd = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pwd.clear()
    pwd.send_keys(PASSWORD)

# TC_Phone_Empty — để trống trường Phone
def test_phone_empty():
    print("\n🧪 TC_Phone_Empty — Để trống trường Phone")
    
    phone = wait.until(EC.visibility_of_element_located((By.NAME, "phone")))
    phone.clear()  # xóa dữ liệu
    fill_required_password()  # nhập mật khẩu để submit form
    click_update_profile()
    
    try:
        error_msg = driver.execute_script("return arguments[0].validationMessage;", phone)
        if error_msg:
            print("✅ Hiển thị thông báo yêu cầu nhập:", error_msg)
        else:
            print("❌ Không hiển thị thông báo tooltip")
    except Exception as e:
        print("❌ Lỗi khi lấy validationMessage:", e)

# TC_Phone_Char — nhập chữ vào trường Phone
def test_phone_char():
    print("\n🧪 TC_Phone_Char — Nhập chữ vào trường Phone")
    
    phone = wait.until(EC.visibility_of_element_located((By.NAME, "phone")))
    phone.clear()
    phone.send_keys("abc")  # thử nhập chữ
    fill_required_password()
    click_update_profile()
    
    # Kiểm tra input vẫn rỗng vì hệ thống chặn chữ
    val = phone.get_attribute("value")
    if val == "":
        print("✅ Hệ thống không cho nhập chữ vào trường Phone")
    else:
        print(f"❌ Hệ thống sai, value hiện tại: {val}")
# TC_Phone_Valid — nhập số điện thoại hợp lệ
def test_phone_valid():
    print("\n🧪 TC_Phone_Valid — Nhập số điện thoại hợp lệ")
    
    phone = wait.until(EC.visibility_of_element_located((By.NAME, "phone")))
    phone.clear()
    phone.send_keys("0963462819")
    fill_required_password()
    click_update_profile()
    
    # Kiểm tra thông báo thành công
    try:
        popup = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]")))
        print("✅ Update thành công:", popup.text)
    except:
        print("❌ Không hiển thị thông báo thành công")

open_homepage()
login()
navigate_to_profile_page()
test_phone_empty()
test_phone_char()
test_phone_valid()
driver.quit()