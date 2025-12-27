from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

# ================== CONFIG ==================
HOME_URL = "https://www.phptravels.net"
REPORT_FILE = "TC_29_Cars_Report.html"
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

report_rows = []

# ================== REPORT ==================
def take_screenshot(tc_name):
    path = f"{SCREENSHOT_DIR}/{tc_name}.png"
    driver.save_screenshot(path)
    return path

def log_result(tc, desc, status, img):
    report_rows.append({
        "tc": tc,
        "desc": desc,
        "status": status,
        "img": img
    })

def generate_report():
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TC_29 Cars Travellers Report</title>
<style>
body {{ font-family: Arial; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }}
th {{ background: #f2f2f2; }}
.pass {{ color: green; font-weight: bold; }}
.fail {{ color: red; font-weight: bold; }}
img {{ width: 350px; border: 1px solid #ccc; }}
</style>
</head>
<body>

<h2>TC_29 – Không cho tổng Travellers = 0</h2>
<p>Generated at: {datetime.now()}</p>

<table>
<tr>
<th>Test Case</th>
<th>Description</th>
<th>Status</th>
<th>Screenshot</th>
</tr>
""")
        for r in report_rows:
            cls = "pass" if r["status"] == "PASS" else "fail"
            f.write(f"""
<tr>
<td>{r["tc"]}</td>
<td>{r["desc"]}</td>
<td class="{cls}">{r["status"]}</td>
<td><img src="{r["img"]}"></td>
</tr>
""")
        f.write("""
</table>
</body>
</html>
""")

# ================== COMMON ==================
def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def navigate_to_cars_page():
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'/cars')]"))
    ).click()
    wait.until(EC.url_contains("cars"))

# ================== LOCATION ==================
def select_from_airport():
    dropdown = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[@id='select2--container']/ancestor::span[@role='combobox']"
    )))
    dropdown.click()

    search_box = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//input[@class='select2-search__field']"
    )))
    search_box.send_keys("DXB")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable((
        By.XPATH, "//ul[contains(@class,'select2-results__options')]/li[1]"
    ))).click()

def select_to_location():
    dropdown = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[@class='input-items cars_location']//span[@role='combobox']"
    )))
    dropdown.click()

    search_box = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//input[@class='select2-search__field']"
    )))
    search_box.send_keys("Lon")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable((
        By.XPATH, "//ul[contains(@class,'select2-results__options')]/li[1]"
    ))).click()

# ================== TRAVELLERS ==================
def open_travellers_dropdown():
    box = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='cars_adults']/ancestor::div[contains(@class,'dropdown-contain')]")
    ))
    box.click()
    time.sleep(0.3)

def js_click(xpath):
    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", el)
    time.sleep(0.2)

def get_adults():
    return int(driver.find_element(By.ID, "cars_adults").get_attribute("value"))

def get_childs():
    return int(driver.find_element(By.ID, "cars_child").get_attribute("value"))

def decrease_adult():
    js_click("(//div[contains(@class,'qtyDec')])[1]")

def decrease_child():
    js_click("(//div[contains(@class,'qtyDec')])[2]")

# ================== TEST CASE ==================
def test_TC_29_no_zero_total():
    tc = "TC_29"
    desc = "Không cho tổng Travellers = 0"

    open_travellers_dropdown()

    while get_adults() > 0:
        decrease_adult()

    while get_childs() > 0:
        decrease_child()

    adults = get_adults()
    childs = get_childs()
    print(f"Adults={adults}, Childs={childs}")

    search_btn = driver.find_element(
        By.XPATH, "//button[@type='submit' and contains(@class,'search_button')]"
    )
    search_btn.click()
    time.sleep(1)

    screenshot = take_screenshot(tc)

    if "cars" in driver.current_url:
        log_result(tc, desc, "FAIL", screenshot)
        print("❌ TC_29 FAIL: Vẫn cho search khi tổng = 0")
    else:
        log_result(tc, desc, "PASS", screenshot)
        print("✅ TC_29 PASS: Hệ thống chặn tổng = 0")

# ================== RUN ==================
open_homepage()
navigate_to_cars_page()
select_from_airport()
select_to_location()
test_TC_29_no_zero_total()

generate_report()
driver.quit()
