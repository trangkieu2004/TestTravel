from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os

# ================== CẤU HÌNH ==================
HOME_URL = "https://www.phptravels.net"
EMAIL = "user@phptravels.com"
PASSWORD = "demouser"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ================== THƯ MỤC LƯU SCREENSHOT ==================
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ================== KẾT QUẢ TEST ==================
test_results = []

# ================== HÀM CHUNG ==================
def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def login():
    driver.get(f"{HOME_URL}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "submitBTN").click()
    wait.until(EC.url_contains("dashboard"))

def navigate_to_profile_page():
    cars_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='My Profile']]")))
    cars_link.click()
    wait.until(EC.url_contains("profile"))

def click_update_profile():
    update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Update Profile')]")))
    update_btn.click()
    time.sleep(1)

def fill_required_password():
    pwd = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pwd.clear()
    pwd.send_keys(PASSWORD)

# ================== HÀM LƯU KẾT QUẢ TEST ==================
def record_result(name, status, message="", screenshot=None):
    test_results.append({
        "name": name,
        "status": status,
        "message": message,
        "screenshot": screenshot
    })

# ================== TEST CASE ==================
def test_TC5_empty_firstname():
    name = "TC_5 — Empty First Name"
    try:
        fn = wait.until(EC.visibility_of_element_located((By.NAME, "first_name")))
        fn.clear()
        fill_required_password()
        click_update_profile()
        error_msg = fn.get_attribute("validationMessage")
        if "Please fill out this field" in error_msg or "Vui lòng" in error_msg:
            record_result(name, "Passed", "Hiển thị thông báo bắt buộc")
        else:
            record_result(name, "Failed", f"Thông báo không đúng: {error_msg}")
    except Exception as e:
        screenshot = os.path.join(SCREENSHOT_DIR, "TC5.png")
        driver.save_screenshot(screenshot)
        record_result(name, "Failed", f"Lỗi: {e}", screenshot)

def test_TC6_space_firstname():
    name = "TC_6 — Space First Name"
    try:
        fn = wait.until(EC.visibility_of_element_located((By.NAME, "first_name")))
        fn.clear()
        fn.send_keys("   ")
        fill_required_password()
        click_update_profile()
        error_msg = fn.get_attribute("validationMessage")
        if "Please fill out this field" in error_msg or "Vui lòng" in error_msg:
            record_result(name, "Passed", "Space bị xem là trống")
        else:
            record_result(name, "Failed", f"Thông báo không đúng: {error_msg}")
    except Exception as e:
        screenshot = os.path.join(SCREENSHOT_DIR, "TC6.png")
        driver.save_screenshot(screenshot)
        record_result(name, "Failed", f"Lỗi: {e}", screenshot)

def test_TC7_valid_firstname():
    name = "TC_7 — Valid First Name"
    try:
        fn = wait.until(EC.visibility_of_element_located((By.NAME, "first_name")))
        fn.clear()
        fn.send_keys("Ali")
        fill_required_password()
        click_update_profile()
        popup_title = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]//h4")
            )
        )
        popup_msg = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'vt-card') and contains(@class,'success')]//p")
            )
        )
        record_result(name, "Passed", f"Popup: {popup_title.text} — {popup_msg.text}")
    except Exception as e:
        screenshot = os.path.join(SCREENSHOT_DIR, "TC7.png")
        driver.save_screenshot(screenshot)
        record_result(name, "Failed", f"Lỗi: {e}", screenshot)

# ================== RUN TEST ==================
try:
    open_homepage()
    login()
    navigate_to_profile_page()
    test_TC5_empty_firstname()
    test_TC6_space_firstname()
    test_TC7_valid_firstname()
finally:
    driver.quit()

# ================== TẠO HTML REPORT ==================
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Selenium Test Report</title>
<style>
body {{ font-family: Arial, sans-serif; background-color: #1e1e1e; color: #eee; }}
h1 {{ color: #00ffcc; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
th, td {{ border: 1px solid #555; padding: 8px; text-align: left; }}
th {{ background-color: #333; color: #fff; }}
tr:nth-child(even) {{ background-color: #2a2a2a; }}
tr:hover {{ background-color: #444; }}
.passed {{ color: #0f0; font-weight: bold; }}
.failed {{ color: #f00; font-weight: bold; }}
img {{ max-width: 300px; border: 1px solid #666; margin-top: 5px; }}
</style>
</head>
<body>
<h1>Test Report — Selenium PHP Travels</h1>
<p>Ngày tạo: {datetime.datetime.now()}</p>

<table>
<tr>
<th>Test Case</th>
<th>Status</th>
<th>Message</th>
<th>Screenshot</th>
</tr>
"""

for t in test_results:
    status_class = "passed" if t["status"].lower() == "passed" else "failed"
    screenshot_html = f"<img src='{t['screenshot']}'>" if t.get("screenshot") else ""
    html += f"<tr><td>{t['name']}</td><td class='{status_class}'>{t['status']}</td><td>{t['message']}</td><td>{screenshot_html}</td></tr>"

html += "</table></body></html>"

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML Report đã tạo xong: report.html")
