from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import datetime

# ================== CONFIG ==================
HOME_URL = "https://www.phptravels.net"
EMAIL = "user@phptravels.com"
PASSWORD = "demouser"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
REPORT_FILE = os.path.join(BASE_DIR, "City.html")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

report_rows = []

CITY_XPATH = "//input[@name='city']"

# ================== UTILS ==================
def take_screenshot(tc_id):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tc_id}_{timestamp}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(path)
    return f"screenshots/{filename}"

def add_report(tc_id, desc, expected, actual, status, screenshot):
    report_rows.append(f"""
        <tr>
            <td>{tc_id}</td>
            <td>{desc}</td>
            <td>{expected}</td>
            <td>{actual}</td>
            <td class="{status.lower()}">{status}</td>
            <td><img src="{screenshot}" width="300"></td>
        </tr>
    """)

def write_report():
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    html = f"""
    <html>
    <head>
        <title>City Validation Report</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background: #f2f2f2; }}
            .pass {{ color: green; font-weight: bold; }}
            .fail {{ color: red; font-weight: bold; }}
            img {{ border: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>CITY FIELD VALIDATION REPORT</h1>
        <p><b>Thời gian chạy:</b> {now}</p>

        <table>
            <tr>
                <th>TC ID</th>
                <th>Mô tả</th>
                <th>Kết quả mong đợi</th>
                <th>Kết quả thực tế</th>
                <th>Trạng thái</th>
                <th>Screenshot</th>
            </tr>
            {''.join(report_rows)}
        </table>
    </body>
    </html>
    """
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

# ================== COMMON ==================
def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def login():
    driver.get(f"{HOME_URL}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "submitBTN").click()
    wait.until(EC.url_contains("dashboard"))

def navigate_to_profile():
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='My Profile']]"))
    ).click()
    wait.until(EC.url_contains("profile"))

def click_update():
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Update Profile')]"))
    ).click()
    time.sleep(1)

def fill_password():
    pwd = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pwd.clear()
    pwd.send_keys(PASSWORD)

# ================== TEST CASES ==================
def TC_26_empty_city():
    tc = "TC_26"
    city = wait.until(EC.visibility_of_element_located((By.XPATH, CITY_XPATH)))
    city.clear()

    fill_password()
    click_update()

    screenshot = take_screenshot(tc)
    msg = city.get_attribute("validationMessage")

    if msg:
        add_report(
            tc,
            "Để trống trường City",
            "Hiển thị thông báo: Vui lòng điền vào trường này",
            msg,
            "PASS",
            screenshot
        )
    else:
        add_report(
            tc,
            "Để trống trường City",
            "Hiển thị thông báo yêu cầu nhập",
            "Không hiển thị thông báo",
            "FAIL",
            screenshot
        )

def TC_27_space_city():
    tc = "TC_27"
    city = wait.until(EC.visibility_of_element_located((By.XPATH, CITY_XPATH)))
    city.clear()
    city.send_keys("   ")

    fill_password()
    click_update()

    screenshot = take_screenshot(tc)
    popup = driver.find_elements(
        By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]"
    )

    if popup:
        add_report(
            tc,
            "Nhập toàn ký tự trắng vào City",
            "Không cho phép update",
            "Vẫn update thành công",
            "FAIL",
            screenshot
        )
    else:
        add_report(
            tc,
            "Nhập toàn ký tự trắng vào City",
            "Hiển thị thông báo yêu cầu nhập",
            "Không update",
            "PASS",
            screenshot
        )

def TC_28_valid_city():
    tc = "TC_28"
    city = wait.until(EC.visibility_of_element_located((By.XPATH, CITY_XPATH)))
    city.clear()
    city.send_keys("Hanoi")

    fill_password()
    click_update()

    screenshot = take_screenshot(tc)

    try:
        popup = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]")
            )
        )
        add_report(
            tc,
            "Nhập City hợp lệ",
            "Hiển thị popup cập nhật thành công",
            "Popup Information Updated hiển thị",
            "PASS",
            screenshot
        )
    except:
        add_report(
            tc,
            "Nhập City hợp lệ",
            "Hiển thị popup cập nhật thành công",
            "Không xuất hiện popup",
            "FAIL",
            screenshot
        )

# ================== RUN ==================
try:
    open_homepage()
    login()
    navigate_to_profile()

    TC_26_empty_city()
    TC_27_space_city()
    TC_28_valid_city()

finally:
    write_report()
    driver.quit()
