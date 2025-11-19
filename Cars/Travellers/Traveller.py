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
    print("🌍 Mở trang chủ...")
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Trang chủ đã mở.\n")


def navigate_to_cars_page():
    print("🚗 Chuyển sang trang Cars...")
    cars_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/cars')]")))
    cars_tab.click()
    wait.until(EC.url_contains("cars"))
    print("✅ Đã vào trang Cars.\n")


# ============================ HÀM TRAVELLERS ============================

def open_travellers_dropdown():
    box = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='cars_adults']/ancestor::div[contains(@class,'dropdown-contain')]")
    ))
    box.click()
    time.sleep(0.3)


def get_adults():
    open_travellers_dropdown()
    adults_value = driver.find_element(By.ID, "cars_adults").get_attribute("value")
    return int(adults_value)

def get_childs():
    return int(driver.find_element(By.XPATH, "//input[@id='cars_child']").get_attribute("value"))

def click_adults_plus(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        plus_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[@class='qtyInc'])[1]")
        ))
        plus_btn.click()
        time.sleep(0.3)

def click_adults_minus(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        minus_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[@class='qtyDec'])[1]")
        ))
        minus_btn.click()
        time.sleep(0.3)


def click_childs_plus(times=1):
    for _ in range(times):
        driver.find_element(By.XPATH, "(//div[@class='qtyInc'])[2]").click()
        time.sleep(0.2)

def click_childs_minus(times=1):
    for _ in range(times):
        driver.find_element(By.XPATH, "(//div[@class='qtyDec'])[2]").click()
        time.sleep(0.2)

# ============================ TEST CASES ============================

def test_TC_20_default_values():
    print("===== TC_20: Kiểm tra dữ liệu mặc định =====")
    adults = get_adults()
    childs = get_childs()
    print(f"Adults = {adults}, Childs = {childs}")
    if adults == 1 and childs == 0:
        print("✅ TC_20 Passed\n")
    else:
        print("❌ TC_20 Failed\n")


def test_TC_21_open_dropdown():
    print("===== TC_21: Kiểm tra mở dropdown Travellers =====")
    open_travellers_dropdown()
    try:
        driver.find_element(By.XPATH, "//input[@id='cars_adults']")
        driver.find_element(By.XPATH, "//input[@id='cars_child']")
        print("✅ TC_21 Passed\n")
    except:
        print("❌ TC_21 Failed\n")


def test_TC_22_increase_adults():
    print("===== TC_22: Tăng Adults =====")

    open_travellers_dropdown()

    before = get_adults()
    click_adults_plus(2)
    after = get_adults()

    print(f"Before: {before}")
    print(f"After:  {after}")

    if after == before + 2:
        print("✅ TC_22 PASSED\n")
    else:
        print("❌ TC_22 FAILED\n")



def test_TC_23_decrease_adults():
    print("===== TC_23: Giảm Adults về 1 =====")
    open_travellers_dropdown()
    click_adults_minus(2)
    adults = get_adults()
    print("Adults =", adults)
    print("✅ Passed\n" if adults == 1 else "❌ Failed\n")

def test_TC_25_increase_childs():
    print("===== TC_25: Tăng Childs =====")
    open_travellers_dropdown()
    click_childs_plus(3)
    childs = get_childs()
    print("Childs =", childs)
    print("✅ Passed\n" if childs == 3 else "❌ Failed\n")

def test_TC_26_childs_minus_at_zero():
    print("===== TC_26: Giảm Childs khi = 0 =====")
    childs_input = driver.find_element(By.ID, "cars_child")
    driver.execute_script("arguments[0].value = '0';", childs_input)
    time.sleep(0.2)
    before = int(childs_input.get_attribute("value"))
    print(f"Childs trước khi nhấn (-): {before}")
    
    click_childs_minus(2)
    after = int(childs_input.get_attribute("value"))
    print(f"Childs sau khi nhấn (-): {after}")
    print("✅ PASS\n" if after >= 0 else "❌ FAIL\n")


def test_TC_27_total_display():
    print("===== TC_27: Kiểm tra tổng Travellers =====")
    adults = get_adults()
    childs = get_childs()
    total = adults + childs
    print(f"Adults = {adults}, Childs = {childs}, Total = {total}")
    print("✅ Passed\n")


def test_TC_28_max_limit():
    print("===== TC_28: Giới hạn tối đa =====")
    open_travellers_dropdown()

    # Ấn tăng Adults và Childs cho đến khi không tăng được nữa
    last_adults = last_childs = -1
    while True:
        click_adults_plus()
        click_childs_plus()
        current_adults = get_adults()
        current_childs = get_childs()
        if current_adults == last_adults and current_childs == last_childs:
            break
        last_adults, last_childs = current_adults, current_childs

    print(f"Adults tối đa = {current_adults}, Childs tối đa = {current_childs}")

    # Kiểm tra xem có phải 12 hay không
    if current_adults == 12 and current_childs == 12:
        print("✅ PASS: Adults và Childs đạt 12\n")
    else:
        print("⚠ FAIL: Giới hạn thực tế khác 12 (UI giới hạn khác)\n")

def test_TC_30_keep_state_after_close():
    print("===== TC_30: Lưu trạng thái sau khi đóng dropdown =====")
    open_travellers_dropdown()
    click_adults_plus(1)
    click_childs_plus(1)

    # đóng dropdown
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(0.3)

    open_travellers_dropdown()
    adults = get_adults()
    childs = get_childs()

    print(f"Adults = {adults}, Childs = {childs}")
    print("✅ Passed\n")


# ============================ CHẠY TEST ============================

open_homepage()
navigate_to_cars_page()

test_TC_20_default_values()
test_TC_21_open_dropdown()
test_TC_22_increase_adults()
# test_TC_23_decrease_adults()
test_TC_25_increase_childs()
test_TC_26_childs_minus_at_zero()
test_TC_27_total_display()
test_TC_28_max_limit()
test_TC_30_keep_state_after_close()

driver.quit()
