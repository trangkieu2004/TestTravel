from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# ===================== CẤU HÌNH CHUNG =====================
HOME_URL = "https://www.phptravels.net"
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ===================== HÀM CHUNG =====================
def open_homepage():
  # Bước 1: Truy cập trang chủ

  print("Truy cập trang chủ")
  driver.get(HOME_URL)
  wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
  print("✅ Đã mở trang chủ PHPTravels.")

# Bước 2: Nhấn vào menu Cars để chuyển hướng sang trang /cars

def navigate_to_cars_page():
    print("Đang chuyển sang trang Cars...")
    cars_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/cars')]")
    ))
    cars_link.click()

    # Chờ đến khi trang Cars tải xong
    wait.until(EC.url_contains("cars"))
    print("✅ Đã vào trang Cars:", driver.current_url)


def open_from_airport_dropdown():
  # Bước #: Mở dropdown From Airport
  print("\n Mở dropdown 'From Airport'...")
  dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@id='select2--container']/ancestor::span[@role='combobox']")))
  dropdown.click()
  return wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='select2-search__field']")))

# ===================== TEST CASE 1 =====================
def test_valid_search_input(search_box):
    """Nhập >=3 ký tự → có kết quả"""
    test_input = "New"
    print(f"\n🔍 [TC01] Tìm kiếm hợp lệ với '{test_input}'...")
    search_box.send_keys(test_input)
    time.sleep(2)

    airports = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//ul[@id='select2--results']//li[contains(@class,'select2-results__option')]")))

    if len(airports) > 0:
        print(f"✅ PASSED: Có {len(airports)} kết quả hiển thị khi nhập '{test_input}'")
    else:
        print(f"❌ FAILED: Không có kết quả hiển thị khi nhập '{test_input}'")
    return airports

# ===================== TEST CASE 2 =====================
def test_invalid_short_input(search_box):
    """Nhập <3 ký tự → Hiển thị thông báo 'Please enter 1 (2,3) or more characters'"""
    print(f"\n🔍 [TC02] Tìm kiếm không hợp lệ (<3 ký tự)...")

    # Nhập ít hơn 3 ký tự (ví dụ: "N")
    search_box.clear()
    search_box.send_keys("N")
    time.sleep(1.5)

    try:
        # Select2 hiển thị thông báo khi nhập <3 ký tự
        message_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//li[contains(@class,'select2-results__message') and contains(text(),'Please enter')]")
        ))
        print(f"✅ PASSED: Hiển thị thông báo '{message_element.text}'")
    except Exception:
        print("⚠ FAILED: Không hiển thị thông báo 'Please enter 1 (2,3) or more characters'")

# ===================== TEST CASE 3 =====================

def test_no_results_found(search_box):
    """Nhập ký tự đặc biệt hoặc từ không tồn tại → Hiển thị thông báo 'No results found'"""
    print(f"\n🔍 [TC03] Kiểm tra nhập dữ liệu không tồn tại hoặc ký tự đặc biệt...")

    test_inputs = ["@@@", "zzzzzz", "!@#$$%", "abcxyz123"]
    for test_input in test_inputs:
        search_box.clear()
        search_box.send_keys(test_input)
        time.sleep(2)

        try:
            message_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'select2-results__message') and text()='No results found']")))
            print(f"✅ PASSED: '{test_input}' → Hiển thị thông báo '{message_element.text}'")
        except Exception:
            print(f"⚠ FAILED: '{test_input}' → Không hiển thị thông báo 'No results found'")

# ===================== TEST CASE 4 =====================
def test_reload_list(search_box):
    """Xóa dữ liệu → click ra ngoài → mở lại dropdown → kiểm tra danh sách hiển thị lại"""
    print(f"\n🔁 [TC04] Xóa dữ liệu và kiểm tra danh sách hiển thị lại...")

    # Xóa dữ liệu
    search_box.clear()
    time.sleep(1)

    # Click ra ngoài để đóng dropdown
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(1)

    # Mở lại dropdown (trả về ô nhập mới)
    search_box = open_from_airport_dropdown()

    # --- Đợi danh sách sân bay hiển thị ---
    airports = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//ul[@id='select2--results']//div[contains(@class,'to--insert')]")))

    # Kiểm tra xem dropdown có dữ liệu không
    if len(airports) > 0:
        print(f"✅ PASSED: Danh sách hiển thị lại với {len(airports)} sân bay")
    else:
        print("❌ FAILED: Không hiển thị lại danh sách sân bay!")
        return []

    # --- Lấy dữ liệu chi tiết từng sân bay ---
    airport_data = []
    for airport in airports:
        code = airport.find_element(By.XPATH, ".//button").text.strip()

        strong_el = airport.find_element(By.XPATH, ".//strong")
        strong_text = strong_el.get_attribute("textContent").strip()
        parts = strong_text.split()
        city = parts[0]
        country = parts[-2] + " " + parts[-1] if len(parts) > 2 else ""
        fullname = airport.find_element(By.XPATH, ".//small[contains(@class, 'airport--name')]").text.strip()

        airport_data.append((airport, code, city, country, fullname))
        print(f"🔁 {code} | {city}, {country} | {fullname}")

    return airport_data

# ===================== TEST CASE 5 =====================

def test_select_random_airport(airport_data):
    """
    Chọn ngẫu nhiên một sân bay từ danh sách airport_data,
    click chọn và kiểm tra giá trị hiển thị trong ô 'From Airport'.
    
    Parameters:
        airport_data (list): Danh sách tuple (airport_element, code, city, country, fullname)
    
    Returns:
        dict: Thông tin sân bay đã chọn
    """
    # --- Chọn ngẫu nhiên 1 option ---
    chosen_airport, chosen_code, chosen_city, chosen_country, chosen_fullname = random.choice(airport_data)
    print(f"\n🎯 Đang chọn sân bay: {chosen_code} - {chosen_fullname}")

    # --- Click chọn option đó ---
    chosen_airport.click()
    time.sleep(2)  # chờ cập nhật giá trị hiển thị

    # --- Kiểm tra giá trị hiển thị trong ô From Airport ---
    selected_value = driver.find_element(By.XPATH, "//span[@id='select2--container']").text.strip()
    print(f"🧩 Giá trị hiển thị sau khi chọn: {selected_value}")

    # --- Kiểm thử kết quả ---
    if (chosen_code in selected_value) or (chosen_city in selected_value) or (chosen_fullname.split()[0] in selected_value):
        print("✅ Kiểm tra chọn option hiển thị đúng: PASSED")
        status = True
    else:
        print("❌ Kiểm tra chọn option hiển thị đúng: FAILED")
        status = False

    # --- Trả về thông tin sân bay đã chọn ---
    return {
        "element": chosen_airport,
        "code": chosen_code,
        "city": chosen_city,
        "country": chosen_country,
        "fullname": chosen_fullname,
        "displayed_value": selected_value,
        "status": status
    }

# ===================== TEST CASE 6 =====================
def test_empty_from_airport():
    """Kiểm tra bỏ trống From Airport và click Search"""
    print("\n🚫 [TC05] Kiểm tra để trống From Airport và click Search...")

    # Làm mới trang để reset form
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
    time.sleep(2)

    # Click nút Search
    search_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class,'search_button')]")
    search_button.click()
    time.sleep(1)

    # Xử lý alert
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"⚠ Alert hiển thị: {alert_text}")

    if "Select From Airport" in alert_text:
        print("✅ PASSED: Alert đúng nội dung 'Select From Airport'")
    else:
        print("❌ FAILED: Nội dung alert không đúng")

    alert.accept()



# ===================== MAIN FLOW =====================
try:
  open_homepage()
  navigate_to_cars_page()

  # Tiếp tục các test case trên trang Cars
  search_box = open_from_airport_dropdown()
  airports = test_valid_search_input(search_box)
  test_invalid_short_input(search_box)
  test_no_results_found(search_box)
  airports = test_reload_list(search_box)
  # Test case 5: Chọn ngẫu nhiên 1 sân bay từ danh sách
  selected_airport_info = test_select_random_airport(airports)
  print(f"\n✅ Sân bay đã chọn: {selected_airport_info['code']} - {selected_airport_info['fullname']}")
  print(f"Giá trị hiển thị trong ô: {selected_airport_info['displayed_value']}")
  print(f"Trạng thái kiểm thử: {'PASSED' if selected_airport_info['status'] else 'FAILED'}")
  test_empty_from_airport()


except Exception as e:
  import traceback
  print("Lỗi trong quá trình test")
  traceback.print_exc()

finally:
  driver.quit()
  print("\n Kiểm thử hoàn tất")