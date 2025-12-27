from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, datetime

# ================== CẤU HÌNH ==================
HOME_URL = "https://www.phptravels.net"
EMAIL = "user@phptravels.com"
PASSWORD = "demouser"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# ================== REPORT ==================
REPORT_FILE = "report_profile_password.html"
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
report_rows = []

def take_screenshot(tc_id, status):
    filename = f"{tc_id}_{status}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(path)
    return path

def add_report(tc_id, description, expected, actual, status, screenshot):
    report_rows.append({
        "tc_id": tc_id,
        "description": description,
        "expected": expected,
        "actual": actual,
        "status": status,
        "screenshot": screenshot
    })

def generate_report():
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head>
            <title>Profile Password Test Report</title>
            <style>
                body {{ font-family: Arial; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; }}
                th {{ background: #f2f2f2; }}
                .PASS {{ color: green; font-weight: bold; }}
                .FAIL {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
        <h2>Profile Password Automation Test Report</h2>
        <p>Generated at: {datetime.datetime.now()}</p>
        <table>
        <tr>
            <th>TC ID</th>
            <th>Description</th>
            <th>Expected</th>
            <th>Actual</th>
            <th>Status</th>
            <th>Screenshot</th>
        </tr>
        """)
        for r in report_rows:
            f.write(f"""
            <tr>
                <td>{r['tc_id']}</td>
                <td>{r['description']}</td>
                <td>{r['expected']}</td>
                <td>{r['actual']}</td>
                <td class="{r['status']}">{r['status']}</td>
                <td><a href="{r['screenshot']}">View</a></td>
            </tr>
            """)
        f.write("</table></body></html>")

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
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='My Profile']]"))).click()
    wait.until(EC.url_contains("profile"))

def click_update_profile():
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Update Profile')]"))).click()
    time.sleep(1)

# ================== TEST CASES ==================

def test_password_hidden_on_load():
    tc = "TC_PW_1"
    pwd = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    if pwd.get_attribute("type") == "password":
        img = take_screenshot(tc, "PASS")
        add_report(tc, "Password hidden on load", "Password masked", "Password masked", "PASS", img)
    else:
        img = take_screenshot(tc, "FAIL")
        add_report(tc, "Password hidden on load", "Password masked", "Password visible", "FAIL", img)

def test_empty_password():
    tc = "TC_PW_empty"
    pw = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pw.clear()
    click_update_profile()
    msg = pw.get_attribute("validationMessage")
    if msg:
        img = take_screenshot(tc, "PASS")
        add_report(tc, "Submit empty password", "Show validation", msg, "PASS", img)
    else:
        img = take_screenshot(tc, "FAIL")
        add_report(tc, "Submit empty password", "Show validation", "No validation", "FAIL", img)

# TC_13 — Cập nhật profile KHÔNG nhập Password (Expected FAIL)
def test_TC_13_update_without_password():
    print("\n🧪 TC_13 — Cập nhật profile KHÔNG nhập Password (Expected FAIL)")

    # 👉 GIỮ NGUYÊN LOGIC CŨ: KHÔNG ĐỤNG VÀO FIELD KHÁC

    # Để trống Password
    pw = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pw.clear()

    # Nhấn Update Profile
    click_update_profile()

    # Kiểm tra validation giống test bỏ trống password
    try:
        error_msg = pw.get_attribute("validationMessage")
        if error_msg:
            print("❌ TC_13 FAIL (ĐÚNG KỲ VỌNG)")
            print("➜ System bắt buộc nhập Password")
            print("➜ Validation message:", error_msg)
        else:
            print("❌ TC_13 FAIL")
            print("➜ Không update nhưng cũng không có validation message")
    except:
        print("❌ TC_13 FAIL")
        print("➜ Không cho phép update khi không nhập Password")


def test_submit_with_old_password():
    tc = "TC_PW_old"
    pw = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pw.clear()
    pw.send_keys(PASSWORD)
    click_update_profile()

    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'success')]")))
        img = take_screenshot(tc, "PASS")
        add_report(tc, "Submit with old password", "Update success", "Update success", "PASS", img)
    except:
        img = take_screenshot(tc, "FAIL")
        add_report(tc, "Submit with old password", "Update success", "No success popup", "FAIL", img)

# ================== RUN ==================
open_homepage()
login()
navigate_to_profile_page()

test_password_hidden_on_load()
test_empty_password()
test_TC_13_update_without_password()
test_submit_with_old_password()

generate_report()
driver.quit()
