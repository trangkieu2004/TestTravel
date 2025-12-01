from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================== CONFIG ==================
HOME_URL = "https://www.phptravels.net"
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ================== COMMON ==================
def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def navigate_to_visa_page():
    visa_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/visa')]"))
    )
    visa_link.click()
    wait.until(EC.url_contains("visa"))

def check_from_country_tooltip():
    """
    Kiểm tra tooltip 'Vui lòng chọn một mục trong danh sách' khi để trống From Country.
    """
    # Nhấn nút Search
    search_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class,'search_button')]"))
    )
    search_btn.click()

    # Chờ tooltip xuất hiện (nếu có)
    try:
        tooltip = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Vui lòng chọn')]"))
        )
        print("⚠️ Tooltip hiển thị:", tooltip.text)
        return True
    except:
        print("✅ Không thấy tooltip xuất hiện.")
        return False

# ================== USAGE ==================
open_homepage()
navigate_to_visa_page()
check_from_country_tooltip()
