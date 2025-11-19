from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

HOME_URL = "https://www.phptravels.net"

# ============================ HÀM CHUNG ============================

def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def navigate_to_cars_page():
    cars_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/cars')]")))
    cars_tab.click()
    wait.until(EC.url_contains("cars"))

def open_travellers_dropdown():
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown dropdown-contain']")))
    dropdown.click()
    time.sleep(0.5)  # đợi dropdown render xong

# ============================ TC_24 ============================

def test_TC_24_adults_minus_twice():
    print("===== TC_24: Nhấn (-) 2 lần khi Adults = 1 =====")

    # Mở dropdown Travellers
    open_travellers_dropdown()

    # Đảm bảo Adults = 1 trước khi test
    adults_input = wait.until(EC.presence_of_element_located((By.ID, "cars_adults")))
    driver.execute_script("arguments[0].value = '1';", adults_input)
    time.sleep(0.2)

    before = int(adults_input.get_attribute("value"))
    print(f"Giá trị trước khi nhấn (-): {before}")

    # Tìm nút (-) của Adults
    minus_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='cars_adults']/preceding-sibling::div[@class='qtyDec']")
    ))

    # Nhấn 2 lần
    for i in range(2):
        driver.execute_script("arguments[0].click();", minus_btn)
        time.sleep(0.2)

    # Lấy giá trị sau khi click
    after = int(adults_input.get_attribute("value"))
    print(f"Giá trị sau khi nhấn (-) 2 lần: {after}")

    # Kiểm tra pass/fail
    if after >= 0:
        print("✅ PASS: Adults >= 0")
    else:
        print("❌ FAIL: Adults < 0 (BUG!)")




# ============================ CHẠY TEST ============================

open_homepage()
navigate_to_cars_page()
test_TC_24_adults_minus_twice()
driver.quit()
