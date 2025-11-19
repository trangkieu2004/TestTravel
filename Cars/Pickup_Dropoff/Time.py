from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select

# ================== CẤU HÌNH ==================
HOME_URL = "https://www.phptravels.net"

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

# ================== KIỂM TRA PICKUP/DROPOFF TIME ==================
def get_dropdown_options(dropdown_xpath):
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
    dropdown.click()
    time.sleep(0.5)
    options = driver.find_elements(By.XPATH, "//ul[contains(@class,'select2-results__options')]/li")
    values = [opt.text.strip() for opt in options]
    dropdown.click()  # đóng dropdown
    return values

def select_dropdown_item(dropdown_xpath, item_text):
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
    dropdown.click()
    time.sleep(0.5)
    item = wait.until(EC.element_to_be_clickable((
        By.XPATH, f"//ul[contains(@class,'select2-results__options')]/li[normalize-space()='{item_text}']"
    )))
    item.click()
    time.sleep(0.5)
    return item_text

def get_selected_value(dropdown_xpath):
    dropdown = wait.until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))
    return dropdown.text.strip()

# ================== TEST CASES ==================
# --- TC_17: Kiểm tra hiển thị dữ liệu Pickup/Dropoff Time ---
def test_TC_17_check_dropdown_values():
    print("===== TC_17: Kiểm tra dữ liệu hiển thị Pickup/Dropoff Time =====")
    pickup_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='cars_from_time']"))))
    dropoff_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='cars_to_time']"))))

    pickup_values = [opt.text.strip() for opt in pickup_select.options]
    dropoff_values = [opt.text.strip() for opt in dropoff_select.options]

    print(f"Pickup Time options: {pickup_values}")
    print(f"Dropoff Time options: {dropoff_values}")

    if pickup_values and dropoff_values:
        print("✅ TC_17: Các giá trị hiển thị đầy đủ.\n")
    else:
        print("⚠ TC_17: Không hiển thị giá trị.\n")

# --- TC_18: Kiểm tra dữ liệu khi chọn 1 item ---
def test_TC_18_select_item_in_dropdown():
    print("===== TC_18: Kiểm tra khi chọn 1 item trong dropdown =====")
    
    pickup_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='cars_from_time']"))))
    dropoff_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='cars_to_time']"))))

    # Chọn giá trị hợp lệ theo dropdown thực tế
    pickup_select.select_by_visible_text("12:00 PM")
    dropoff_select.select_by_visible_text("14:00 PM")  # sửa từ 02:00 PM -> 14:00 PM

    selected_pickup = pickup_select.first_selected_option.text.strip()
    selected_dropoff = dropoff_select.first_selected_option.text.strip()

    print(f"Selected Pickup Time: {selected_pickup}")
    print(f"Selected Dropoff Time: {selected_dropoff}")

    if selected_pickup == "12:00 PM" and selected_dropoff == "14:00 PM":
        print("✅ TC_18: Giá trị hiển thị đúng.\n")
    else:
        print("⚠ TC_18: Giá trị hiển thị sai.\n")



# --- TC_19: Kiểm tra giá trị mặc định khi mở trang Cars ---
def test_TC_19_default_values():
    print("===== TC_19: Kiểm tra giá trị mặc định Pickup/Dropoff Time =====")
    
    pickup_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='cars_from_time']"))))
    dropoff_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='cars_to_time']"))))
    
    default_pickup = pickup_select.first_selected_option.text.strip()
    default_dropoff = dropoff_select.first_selected_option.text.strip()
    
    print(f"Default Pickup Time: {default_pickup}")
    print(f"Default Dropoff Time: {default_dropoff}")
    
    if default_pickup == "00:00 AM" and default_dropoff == "00:00 AM":
        print("✅ TC_19: Giá trị mặc định đúng là 00:00 AM.\n")
    else:
        print("⚠ TC_19: Giá trị mặc định KHÔNG phải 00:00 AM.\n")


# ================== CHẠY TEST ==================
open_homepage()
navigate_to_cars_page()

test_TC_19_default_values()
test_TC_17_check_dropdown_values()
test_TC_18_select_item_in_dropdown()

driver.quit()
