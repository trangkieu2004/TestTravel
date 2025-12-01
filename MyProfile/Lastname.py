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

# ================== Test case Last Name ==================
# TC_Email — Kiểm tra trường Email có thể chỉnh sửa không
def test_email_readonly():
    print("\n🧪 TC_Email — Kiểm tra trường Email có thể chỉnh sửa không")

    email_input = wait.until(EC.visibility_of_element_located((By.NAME, "email")))

    try:
        # Kiểm tra attribute readonly hoặc disabled
        is_readonly = email_input.get_attribute("readonly")
        is_disabled = email_input.get_attribute("disabled")

        if is_readonly or is_disabled:
            print("✅ Pass: Trường Email bị khóa, không thể chỉnh sửa")
        else:
            # Thử gửi ký tự vào input
            try:
                email_input.clear()
                email_input.send_keys("test@example.com")
                print("❌ Fail: Trường Email có thể chỉnh sửa")
            except:
                print("✅ Pass: Trường Email không thể chỉnh sửa")
    except Exception as e:
        print("❌ Lỗi khi kiểm tra trường Email:", e)


# TC_5_LN — Bỏ trống Last Name
def test_TC5_empty_lastname():
    print("\n🧪 TC_5_LN — Để trống Last Name")

    ln = wait.until(EC.visibility_of_element_located((By.NAME, "last_name")))
    ln.clear()

    fill_required_password()      # ⭐ BẮT BUỘC
    click_update_profile()

    try:
        error_msg = ln.get_attribute("validationMessage")
        if "Please fill out this field" in error_msg or "Vui lòng" in error_msg:
            print("✅ Đúng: Hiển thị thông báo yêu cầu nhập")
        else:
            print("❌ Sai: Không hiển thị thông báo đúng")
    except:
        print("❌ Không lấy được validationMessage")


# TC_6_LN — Nhập ký tự trắng vào Last Name
def test_TC6_space_lastname():
    print("\n🧪 TC_6_LN — Nhập ký tự trắng vào Last Name")

    ln = wait.until(EC.visibility_of_element_located((By.NAME, "last_name")))
    ln.clear()
    ln.send_keys("   ")

    fill_required_password()      # ⭐ BẮT BUỘC
    click_update_profile()

    try:
        # Kiểm tra popup (giống TC_7)
        popup = driver.find_elements(By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]")
        if popup:
            print("❌ Fail: Popup xuất hiện khi nhập space")
        else:
            error_msg = ln.get_attribute("validationMessage")
            if "Please fill out this field" in error_msg or "Vui lòng" in error_msg:
                print("✅ Pass: Space bị xem là trống, không hiển thị popup")
            else:
                print("❌ Fail: Không báo lỗi đúng")
    except Exception as e:
        print("❌ Lỗi khi kiểm tra TC_6_LN:", e)



# TC_7_LN — Nhập hợp lệ Last Name
def test_TC7_valid_lastname():
    print("\n🧪 TC_7_LN — Nhập hợp lệ 'Ali' vào Last Name")

    ln = wait.until(EC.visibility_of_element_located((By.NAME, "last_name")))
    ln.clear()
    ln.send_keys("Ali")

    fill_required_password()      # ⭐ BẮT BUỘC
    click_update_profile()

    try:
        popup_title = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]//h4")
            )
        )
        popup_msg = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]//p")
            )
        )

        print("✅ Popup Title:", popup_title.text)
        print("✅ Popup Message:", popup_msg.text)

        # Nếu có nút OK, bật code dưới đây
        # ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK')]")))
        # ok_btn.click()

    except Exception as e:
        print("❌ Không xuất hiện popup cập nhật!")
        print("Lỗi:", e)


open_homepage()
login()
navigate_to_profile_page()

test_email_readonly()

test_TC5_empty_lastname()
test_TC6_space_lastname()
test_TC7_valid_lastname()

driver.quit()
