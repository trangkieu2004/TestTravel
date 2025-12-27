from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import os
import datetime

# ================== CONFIG ==================
HOME_URL = "https://www.phptravels.net"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
REPORT_FILE = os.path.join(BASE_DIR, "TC_35.html")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ================== COMMON ==================
def explain(text):
    print(f"▶ {text}")

def open_homepage():
    explain("Mở trang chủ")
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def go_to_visa_page():
    explain("Chuyển sang trang Visa")
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/visa')]"))
    ).click()
    wait.until(EC.url_contains("/visa"))

# ================== COUNTRY ==================
def get_country_options(container_index):
    dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"(//span[@role='combobox'])[ {container_index} ]")
        )
    )
    dropdown.click()
    time.sleep(1)

    items = wait.until(lambda d: d.find_elements(
        By.XPATH,
        "//body//ul[contains(@class,'select2-results__options')]//li[contains(@class,'select2-results__option')]"
    ))

    if not items:
        raise Exception("Không load được country list")

    return items

def select_random_country(items):
    random.choice(items).click()
    time.sleep(1)

# ================== DATE ==================
def enter_travel_date(date_str="04-12-2025"):
    explain("Nhập ngày đi")
    date_input = wait.until(EC.presence_of_element_located((By.ID, "date")))
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
    date_input.clear()
    date_input.send_keys(date_str)

# ================== SEARCH ==================
def click_search():
    explain("Nhấn Search để vào Submission Form")
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    ).click()
    wait.until(EC.url_contains("/visa/submit/"))

# ================== SUBMISSION FORM ==================
def fill_submission_form():
    explain("Điền thông tin cơ bản")
    wait.until(EC.presence_of_element_located((By.NAME, "first_name"))).send_keys("John")
    driver.find_element(By.NAME, "last_name").send_keys("Doe")
    driver.find_element(By.NAME, "email").send_keys("john.doe@example.com")
    driver.find_element(By.NAME, "phone").send_keys("0123456789")

# ================== SCREENSHOT ==================
def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"TC_35_{timestamp}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(path)
    return f"screenshots/{filename}"

# ================== REPORT ==================
def write_html_report(input_value, actual_value, status, screenshot_path):
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    html = f"""
    <html>
    <head>
        <title>Test Report - TC_35</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h1 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 70%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            .fail {{ color: red; font-weight: bold; }}
            .pass {{ color: green; font-weight: bold; }}
            img {{ margin-top: 20px; width: 800px; border: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>TEST CASE: TC_35</h1>
        <p><b>Mô tả:</b> Kiểm tra nhập ký tự chữ vào trường Number of Day</p>
        <p><b>Thời gian chạy:</b> {now}</p>

        <table>
            <tr>
                <th>Giá trị nhập</th>
                <th>Giá trị thực tế</th>
                <th>Trạng thái</th>
            </tr>
            <tr>
                <td>{input_value}</td>
                <td>{actual_value}</td>
                <td class="{ 'fail' if status == 'FAIL' else 'pass' }">{status}</td>
            </tr>
        </table>

        <h3>Screenshot minh chứng</h3>
        <img src="{screenshot_path}">
    </body>
    </html>
    """

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

# ================== TC_35 ==================
def tc_35_number_of_day_accept_text():
    explain("TC_35: Nhập chữ vào Number of Day")

    number_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='number_of_days']"))
    )

    number_input.clear()
    time.sleep(1)

    test_text = "eeeeee"
    number_input.send_keys(test_text)
    time.sleep(1)

    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(1)

    actual_value = number_input.get_attribute("value")

    screenshot = take_screenshot()

    if actual_value == test_text:
        write_html_report(test_text, actual_value, "FAIL", screenshot)
        print("❌ TC_35 FAIL – Trường cho phép nhập ký tự chữ")
    else:
        write_html_report(test_text, actual_value, "PASS", screenshot)
        print("✅ TC_35 PASS")

# ================== FLOW ==================
try:
    open_homepage()
    go_to_visa_page()

    select_random_country(get_country_options(1))
    select_random_country(get_country_options(2))

    enter_travel_date()
    click_search()

    fill_submission_form()

    # ❗ TC_35 – KHÔNG SUBMIT
    tc_35_number_of_day_accept_text()

finally:
    driver.quit()
