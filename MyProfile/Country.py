from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

# ================== Test case Country ==================

# TC_CN_1 — Kiểm tra hiển thị danh sách quốc gia
def test_country_count():
    print("\n🧪 TC_1 — Hiển thị số lượng quốc gia")

    # Mở dropdown
    dropdown_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'dropdown-toggle')]")
        )
    )
    dropdown_btn.click()
    time.sleep(1)  # chờ danh sách load

    # Lấy tất cả các quốc gia trong div.dropdown-menu.show
    country_items = driver.find_elements(By.XPATH, "//div[@class='dropdown-menu show']//span[@class='text']")

    print(f"✅ Tổng số quốc gia hiển thị: {len(country_items)}")
    # In ra 5 quốc gia đầu để kiểm tra
    for c in country_items[:5]:
        print("   -", c.text)

def test_empty_country():
    print("\n🧪 TC_CN_Empty — Không chọn quốc gia")

    # Chọn lại Select Country để reset về trống
    dropdown_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'dropdown-toggle')]"))
    )
    dropdown_btn.click()
    time.sleep(0.5)

    select_default = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='dropdown-menu show']//span[text()='Select Country']")
        )
    )
    select_default.click()
    time.sleep(0.5)

    # Nhấn Update Profile
    fill_required_password()
    click_update_profile()
    time.sleep(0.5)

    # Check validity bằng JS
    try:
        valid = driver.execute_script("""
            var sel = document.querySelector('select[name="country"]');
            if(sel) return sel.checkValidity();
            else return 'no_select';
        """)
        if valid == False:
            print("✅ Pass: Tooltip trình duyệt hiển thị yêu cầu chọn quốc gia")
        elif valid == 'no_select':
            print("❌ Không tìm thấy <select> gốc để check validity")
        else:
            print("❌ Fail: Form có thể submit mà không chọn quốc gia")
    except Exception as e:
        print("❌ Lỗi khi check validity bằng JS:", e)


def test_search_and_select_country():
    print("\n🧪 TC_CN_Search_Select — Nhập 'Vie' và chọn Vietnam")

    # Mở dropdown
    dropdown_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'dropdown-toggle')]"))
    )
    dropdown_btn.click()
    time.sleep(0.3)

    # Lấy menu dropdown hiện tại
    menu_div = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'dropdown-menu') and contains(@class,'show')]"))
    )

    # Lấy search input và nhập 'Vie'
    search_input = menu_div.find_element(By.XPATH, ".//div[@class='bs-searchbox']/input")
    search_input.clear()
    search_input.send_keys("Vie")
    time.sleep(0.3)  # chờ filter

    # Tìm item Viet Nam
    items = menu_div.find_elements(By.XPATH, ".//a[contains(@class,'dropdown-item')]")
    target = None
    for item in items:
        if "Viet Nam" in item.text:
            target = item
            break

    if target:
        # Scroll tới và click
        ActionChains(driver).move_to_element(target).click().perform()
        print("✅ Đã chọn Viet Nam")
    else:
        print("❌ Không tìm thấy Viet Nam")
        return

    # Kiểm tra hiển thị trên form
    displayed = dropdown_btn.find_element(By.CLASS_NAME, "filter-option-inner-inner").text
    print("🔹 Hiển thị trên form:", displayed)



open_homepage()
login()
navigate_to_profile_page()

test_country_count()
test_empty_country()
test_search_and_select_country()

driver.quit()