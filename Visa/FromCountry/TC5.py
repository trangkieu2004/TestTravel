from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# ================== CONFIG ==================
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)
HOME_URL = "https://www.phptravels.net"

# ================== COMMON ==================
def open_homepage():
    print("🌍 Mở trang chủ...")
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Trang chủ đã mở.\n")

def go_to_visa_page():
    print("✈️ Chuyển sang trang Visa...")
    visa_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'/visa')]")
    ))
    visa_link.click()
    wait.until(EC.url_contains("visa"))
    print("✅ Đã vào trang Visa.\n")

# ================== DROPDOWN ==================
def get_country_options():
    """Mở dropdown From Country và trả về danh sách option"""
    # Click vào dropdown (nếu cần)
    container = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//span[@id='select2--container']/ancestor::span[@role='combobox']")
    ))
    container.click()
    
    # Lấy input search field
    search_box = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@class='select2-search__field']")
    ))
    
    # Lấy danh sách tất cả option hiện tại
    items = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//ul[@id='select2--results']//li[contains(@class,'select2-results__option')]")
    ))
    
    # Loại bỏ "No results"
    countries = [(x, x.text.strip()) for x in items if "No results" not in x.text]
    return countries

# ================== SELECT RANDOM ==================
def select_random_country(countries):
    """Chọn ngẫu nhiên 1 quốc gia và kiểm tra hiển thị"""
    chosen_element, country_name = random.choice(countries)
    print(f"\n🌍 Đang chọn quốc gia: {country_name}")
    chosen_element.click()
    time.sleep(1)  # chờ hiển thị update
    
    displayed_value = driver.find_element(By.XPATH, "//span[@id='select2--container']").text.strip()
    print(f"🧩 Giá trị hiển thị: {displayed_value}")
    
    if country_name in displayed_value:
        print("✅ PASSED: Quốc gia hiển thị đúng")
    else:
        print("❌ FAILED: Quốc gia hiển thị sai")
    
    return {
        "element": chosen_element,
        "country_name": country_name,
        "displayed_value": displayed_value
    }

# ================== RUN ==================
open_homepage()
go_to_visa_page()

countries = get_country_options()
select_random_country(countries)

driver.quit()
