from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os

# ================== CONFIG ==================
HOME_URL = "https://www.phptravels.net"
DATE_INPUT_XPATH = "//input[@id='date']"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../.."))
SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "screenshots")
REPORT_FILE = os.path.join(PROJECT_DIR, "TC_15.html")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

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

# ================== SCREENSHOT ==================
def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"TC_15_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    return f"screenshots/{filename}"

# ================== REPORT ==================
def write_html_report(status, actual, expected, screenshot_path):
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    html = f"""
    <html>
    <head>
        <title>Test Report - TC_15</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            .pass {{ color: green; font-weight: bold; }}
            .fail {{ color: red; font-weight: bold; }}
            table {{ border-collapse: collapse; width: 70%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background: #f2f2f2; }}
            img {{ margin-top: 20px; width: 800px; border: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>TEST CASE: TC_15</h1>
        <p><b>Mô tả:</b> Kiểm tra giá trị mặc định của ô Date là ngày hiện tại</p>
        <p><b>Thời gian chạy:</b> {now}</p>

        <table>
            <tr>
                <th>Kết quả mong đợi</th>
                <th>Kết quả thực tế</th>
                <th>Trạng thái</th>
            </tr>
            <tr>
                <td>{expected}</td>
                <td>{actual}</td>
                <td class="{ 'pass' if status == 'PASS' else 'fail' }">{status}</td>
            </tr>
        </table>

        <h3>Screenshot minh chứng</h3>
        <img src="{screenshot_path}">
    </body>
    </html>
    """

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

# ================== TEST ==================
def check_today_in_date_input():
    date_input = wait.until(
        EC.presence_of_element_located((By.XPATH, DATE_INPUT_XPATH))
    )
    actual_value = date_input.get_attribute("value")
    expected_value = datetime.datetime.now().strftime("%d-%m-%Y")

    screenshot = take_screenshot()

    if actual_value == expected_value:
        write_html_report("PASS", actual_value, expected_value, screenshot)
    else:
        write_html_report("FAIL", actual_value, expected_value, screenshot)

# ================== RUN ==================
open_homepage()
navigate_to_visa_page()
check_today_in_date_input()
driver.quit()
