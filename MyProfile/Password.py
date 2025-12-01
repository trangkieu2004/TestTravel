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

# ================== Test case Password ==================

# TC_PW_1 — Kiểm tra ô Password khi mở form
def test_password_hidden_on_load():
    print("\n🧪 TC_PW_1 — Kiểm tra ô Password khi mở form")

    pwd_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    input_type = pwd_input.get_attribute("type")

    if input_type == "password":
        print("✅ Pass: Ô Password không hiển thị ký tự")
    else:
        print("❌ Fail: Ô Password hiển thị ký tự, type =", input_type)

# TC_PW_empty — Bỏ trống Password
def test_empty_password():
    print("\n🧪 TC_PW_empty — Để trống Password")

    pw = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pw.clear()  # Bỏ trống password

    click_update_profile()  # Nhấn Update Profile

    try:
        error_msg = pw.get_attribute("validationMessage")
        if "Please fill out this field" in error_msg or "Vui lòng" in error_msg:
            print("✅ Đúng: Hiển thị thông báo yêu cầu nhập")
        else:
            print("❌ Sai: Không hiển thị thông báo yêu cầu nhập (Password không bắt buộc)")
    except:
        print("❌ Không lấy được validationMessage")


# TC_PW_old — Nhập lại mật khẩu cũ khi cập nhật profile
def test_submit_with_old_password():
    print("\n🧪 TC_PW_old — Nhập mật khẩu cũ và submit")

    # Lấy ô Password
    pw = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pw.clear()
    pw.send_keys("demouser")  # Nhập mật khẩu cũ

    click_update_profile()  # Nhấn Update Profile

    try:
        # Chờ popup thành công giống TC_7
        popup_title = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]//h4"))
        )
        popup_msg = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]//p"))
        )

        print("✅ Popup Title:", popup_title.text)
        print("✅ Popup Message:", popup_msg.text)
        print("✅ Pass: Submit thành công với mật khẩu cũ")
    except Exception as e:
        print("❌ Fail: Không xuất hiện popup cập nhật!", e)


open_homepage()
login()
navigate_to_profile_page()

test_password_hidden_on_load()
test_empty_password()
test_submit_with_old_password()

driver.quit()