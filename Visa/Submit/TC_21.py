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
    wait.until(EC.url_contains("/visa"))
    print("✅ Đã vào trang Visa.\n")

# ================== GET COUNTRY OPTIONS ==================
def get_country_options(container_index):
    """
    Lấy danh sách countries từ Select2 dropdown.
    container_index=1 -> From Country
    container_index=2 -> To Country
    Trả về list of tuples (li_element, country_name, country_code)
    """
    container = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"(//span[@role='combobox'])[ {container_index} ]")
    ))
    container.click()
    time.sleep(1)  # chờ dropdown animation

    items = wait.until(lambda d: d.find_elements(
        By.XPATH, "//body//ul[contains(@class,'select2-results__options')]/li[contains(@class,'select2-results__option')]"
    ))

    countries = []
    for li in items:
        name = li.text.strip()
        li_id = li.get_attribute("id")
        if name and li_id:
            code = li_id.split('-')[-1].lower()  # Ép chữ thường
            countries.append((li, name, code))

    print(f"Container {container_index}: found {len(countries)} countries")
    if not countries:
        raise Exception(f"Không tìm thấy country nào ở container {container_index}")
    return countries

# ================== SELECT RANDOM COUNTRY ==================
def select_random_country(countries, container_index):
    li_element, name, code = random.choice(countries)
    print(f"🌍 Chọn container {container_index}: {name} ({code})")
    li_element.click()
    time.sleep(1)  # chờ dropdown cập nhật

    displayed_value = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(
            By.XPATH, f"(//span[@role='combobox'])[ {container_index} ]/span[@class='select2-selection__rendered']"
        ).text.strip()
    )
    print(f"🧩 Giá trị hiển thị: {displayed_value}\n")
    return name, code

# ================== ENTER DATE ==================
def enter_travel_date(date_str="04-12-2025"):
    print(f"📅 Nhập ngày đi: {date_str}")
    date_input = wait.until(EC.presence_of_element_located((By.ID, "date")))
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
    date_input.clear()
    date_input.send_keys(date_str)
    print("✅ Ngày đã nhập.\n")

# ================== SUBMIT & CHECK URL ==================
def click_submit_and_check_redirect(from_code, to_code, date_str):
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    submit_button.click()
    expected_url = f"https://www.phptravels.net/visa/submit/{from_code}/{to_code}/{date_str}"

    # Chờ URL load xong
    wait.until(EC.url_contains(f"/visa/submit/{from_code}/{to_code}/{date_str}"))
    print(f"✅ URL hiện tại: {driver.current_url}")
    print(f"🔹 URL mong đợi: {expected_url}\n")

# ================== CHECK DISPLAYED VALUES ==================
def check_displayed_values(from_name, to_name, date_str):
    # Chờ phần hiển thị load xong với text khác rỗng
    from_displayed = WebDriverWait(driver, 10).until(
        lambda d: (text:=d.find_element(By.ID, "fetchFrom").text.strip()) != "" and text
    )
    to_displayed = WebDriverWait(driver, 10).until(
        lambda d: (text:=d.find_element(By.ID, "fetchTo").text.strip()) != "" and text
    )
    date_displayed = WebDriverWait(driver, 10).until(
        lambda d: (text:=d.find_element(By.XPATH, "//div[@class='section-heading']//h5").text.strip()) != "" and text
    )

    print(f"From displayed: {from_displayed}")
    print(f"To displayed: {to_displayed}")
    print(f"Date displayed: {date_displayed}")

    # Trang hiển thị đảo ngược From/To
    if from_displayed == to_name.upper() and to_displayed == from_name.upper() and date_displayed == date_str:
        print("✅ Các giá trị hiển thị đúng với lựa chọn ban đầu")
    else:
        print("❌ Giá trị hiển thị KHÔNG đúng!")


# ================== FLOW ==================
open_homepage()
go_to_visa_page()

# Chọn From Country
from_countries = get_country_options(container_index=1)
from_name, from_code = select_random_country(from_countries, container_index=1)

# Chọn To Country
to_countries = get_country_options(container_index=2)
to_name, to_code = select_random_country(to_countries, container_index=2)

# Nhập ngày đi
date_str = "04-12-2025"
enter_travel_date(date_str)

# Nhấn submit và kiểm tra URL
click_submit_and_check_redirect(from_code, to_code, date_str)

# Kiểm tra giá trị hiển thị
check_displayed_values(from_name, to_name, date_str)

driver.quit()
