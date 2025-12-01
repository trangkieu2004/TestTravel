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

def test_profile_information_displayed_correctly():
    print("🧪 Kiểm tra hiển thị đầy đủ và giá trị đúng của thông tin Profile...\n")

    # ====== Danh sách các trường cần hiển thị ======
    required_fields = {
        "First Name": "//input[@name='first_name']",
        "Last Name": "//input[@name='last_name']",
        "Email": "//input[@name='email']",
        "Password": "//input[@name='password']",
        "Country": "//span[contains(text(),'Pakistan')]",
        "Phone": "//input[@name='phone']",
        "State": "//input[@name='state']",
        "City": "//input[@name='city']",
        "Address 1": "//input[@name='address1']",
        "Address 2": "//input[@name='address2']",
        "Update Profile Button": "//button[contains(text(),'Update Profile')]"
    }

    # ====== Kiểm tra hiển thị ======
    print("🔎 Đang kiểm tra các trường có hiển thị không...\n")

    for name, xpath in required_fields.items():
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            print(f"✅ {name} hiển thị OK")
        except:
            print(f"❌ {name} KHÔNG hiển thị !!!")

    print("\n---------------------------------------------\n")

    # ====== Kiểm tra giá trị hiển thị ======
    print("🔎 Đang kiểm tra giá trị có đúng không...\n")

    expected_values = {
        "First Name": ("//input[@name='first_name']", "Demo"),
        "Last Name": ("//input[@name='last_name']", "User"),
        "Email": ("//input[@name='email']", "user@phptravels.com"),
        "Phone": ("//input[@name='phone']", "334411245"),
        "State": ("//input[@name='state']", "punjab"),
        "City": ("//input[@name='city']", "lahore"),
        "Address 1": ("//input[@name='address1']", "New Cavalry Street 6")
    }

    for field_name, (xpath, expected) in expected_values.items():
        element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        value = element.get_attribute("value")

        if value.strip() == expected:
            print(f"✅ {field_name} đúng ({expected})")
        else:
            print(f"❌ {field_name} sai — Expected: {expected}, Actual: {value}")

    print("\n🎉 Hoàn thành kiểm tra Profile!\n")




open_homepage()
login()
navigate_to_profile_page()
test_profile_information_displayed_correctly()
driver.quit()
