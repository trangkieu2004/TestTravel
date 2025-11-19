from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# ===================== CẤU HÌNH CHUNG =====================
HOME_URL = "https://www.phptravels.net"
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ===================== HÀM CHUNG =====================
def open_homepage():
    print("Truy cập trang chủ PHPTravels...")
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Đã mở trang chủ.\n")

def navigate_to_cars_page():
    print("Chuyển sang trang Cars...")
    cars_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/cars')]")
    ))
    cars_link.click()
    wait.until(EC.url_contains("cars"))
    print(f"✅ Đã vào trang Cars: {driver.current_url}\n")

def open_from_airport_dropdown():
    """Mở dropdown 'From Airport' và trả về ô input để nhập"""
    print("\n🛫 Mở dropdown 'From Airport'...")
    dropdown = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[@id='select2--container']/ancestor::span[@role='combobox']"
    )))
    dropdown.click()
    return wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@class='select2-search__field']")
    ))

# ===================== TEST CASE =====================
def test_blank_to_location():
    """[TC14] Nhập From Airport, bỏ trống To Location rồi nhấn Search"""
    print("\n🚀 [TC14] Kiểm tra bỏ trống To Location")

    # --- Mở trang chủ & đi đến trang Cars ---
    open_homepage()
    navigate_to_cars_page()

    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
    time.sleep(2)

    # --- Mở dropdown 'From Airport' ---
    search_box = open_from_airport_dropdown()

    # --- Gõ ký tự 'a' để load danh sách sân bay ---
    search_box.send_keys("new")
    time.sleep(1.5)

    # --- Lấy danh sách các sân bay hiển thị ---
    options = wait.until(EC.presence_of_all_elements_located((
        By.XPATH, "//ul[@id='select2--results']/li[contains(@class,'select2-results__option') and not(contains(@class,'loading-results'))]"
    )))

    if not options:
        print("❌ FAILED: Không tìm thấy sân bay nào trong danh sách!")
        return

    # --- Chọn ngẫu nhiên 1 sân bay ---
    random_option = random.choice(options)
    chosen_text = random_option.text.strip()
    print(f"🎯 Chọn From Airport: {chosen_text}")

    # Cuộn đến phần tử (tránh lỗi không tương tác được)
    driver.execute_script("arguments[0].scrollIntoView(true);", random_option)
    time.sleep(0.5)

    random_option.click()
    time.sleep(1)

    # --- Kiểm tra alert hoặc thông báo lỗi ---
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        if "Select To Location" in alert_text or "Select Drop off location" in alert_text:
            print("✅ PASSED: Hiển thị đúng thông báo yêu cầu chọn To Location.")
        else:
            print(f"❌ FAILED: Sai nội dung thông báo: {alert_text}")
        alert.accept()
    except Exception:
        print("❌ FAILED: Không hiển thị alert khi bỏ trống To Location!")

    print("🏁 Hoàn thành test case TC14.\n")

# ===================== MAIN =====================
if __name__ == "__main__":
    test_blank_to_location()
    driver.quit()
