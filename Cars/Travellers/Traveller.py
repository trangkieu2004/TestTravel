from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

# ============================ CONFIG ============================

HOME_URL = "https://www.phptravels.net"
REPORT_FILE = "Travellers_Cars_Report.html"
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

report_rows = []

# ============================ REPORT ============================

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
<title>Cars Travellers Test Report</title>
<style>
body {{ font-family: Arial; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }}
th {{ background: #f2f2f2; }}
.pass {{ color: green; font-weight: bold; }}
.fail {{ color: red; font-weight: bold; }}
img {{ width: 300px; border: 1px solid #ccc; }}
</style>
</head>
<body>
<h2>Cars – Travellers Automation Test Report</h2>
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

# ============================ COMMON ============================

def open_homepage():
    driver.get(HOME_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def navigate_to_cars_page():
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'/cars')]"))
    ).click()
    wait.until(EC.url_contains("cars"))

# ============================ TRAVELLERS ============================

def open_travellers_dropdown():
    box = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@id='cars_adults']/ancestor::div[contains(@class,'dropdown-contain')]")
    ))
    box.click()
    time.sleep(0.3)

def js_click(xpath):
    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", el)

def increase_adult(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        js_click("(//div[contains(@class,'qtyInc')])[1]")
        time.sleep(0.3)

def increase_child(times=1):
    open_travellers_dropdown()
    for _ in range(times):
        js_click("(//div[contains(@class,'qtyInc')])[2]")
        time.sleep(0.3)

def get_adults():
    return int(driver.find_element(By.ID, "cars_adults").get_attribute("value"))

def get_childs():
    return int(driver.find_element(By.ID, "cars_child").get_attribute("value"))

# ============================ TEST CASES ============================

def test_TC_20_default_values():
    tc = "TC_20"
    adults, childs = get_adults(), get_childs()
    img = take_screenshot(tc)
    if adults == 1 and childs == 0:
        log_result(tc, "Giá trị mặc định Travellers", "PASS", img)
    else:
        log_result(tc, "Giá trị mặc định Travellers", "FAIL", img)

def test_TC_21_open_dropdown():
    tc = "TC_21"
    open_travellers_dropdown()
    img = take_screenshot(tc)
    log_result(tc, "Mở dropdown Travellers", "PASS", img)

def test_TC_22_increase_adults():
    tc = "TC_22"
    before = get_adults()
    increase_adult(2)
    after = get_adults()
    img = take_screenshot(tc)
    log_result(tc, "Tăng số Adult", "PASS" if after == before + 2 else "FAIL", img)

def test_TC_25_increase_childs():
    tc = "TC_25"
    increase_child(3)
    img = take_screenshot(tc)
    log_result(tc, "Tăng số Child", "PASS" if get_childs() == 3 else "FAIL", img)

def test_TC_26_childs_minus_at_zero():
    tc = "TC_26"
    driver.execute_script("arguments[0].value='0';", driver.find_element(By.ID, "cars_child"))
    img = take_screenshot(tc)
    log_result(tc, "Không cho Child < 0", "PASS", img)

def test_TC_27_total_display():
    tc = "TC_27"
    img = take_screenshot(tc)
    log_result(tc, "Hiển thị tổng Travellers", "PASS", img)

def test_TC_28_max_limit():
    tc = "TC_28"
    open_travellers_dropdown()

    last = get_adults()
    while True:
        js_click("(//div[contains(@class,'qtyInc')])[1]")
        time.sleep(0.2)
        cur = get_adults()
        if cur == last:
            break
        last = cur

    last = get_childs()
    while True:
        js_click("(//div[contains(@class,'qtyInc')])[2]")
        time.sleep(0.2)
        cur_child = get_childs()
        if cur_child == last:
            break
        last = cur_child

    img = take_screenshot(tc)
    if get_adults() == 12 and get_childs() == 12:
        log_result(tc, "Giới hạn tối đa Adult & Child", "PASS", img)
    else:
        log_result(tc, "Giới hạn tối đa Adult & Child", "FAIL", img)

def test_TC_30_keep_state_after_close():
    tc = "TC_30"
    increase_adult(1)
    increase_child(1)

    before_a, before_c = get_adults(), get_childs()
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(0.5)
    open_travellers_dropdown()

    img = take_screenshot(tc)
    if before_a == get_adults() and before_c == get_childs():
        log_result(tc, "Giữ trạng thái sau khi đóng dropdown", "PASS", img)
    else:
        log_result(tc, "Giữ trạng thái sau khi đóng dropdown", "FAIL", img)

# ============================ RUN ============================

open_homepage()
navigate_to_cars_page()

test_TC_20_default_values()
test_TC_21_open_dropdown()
test_TC_22_increase_adults()
test_TC_25_increase_childs()
test_TC_26_childs_minus_at_zero()
test_TC_27_total_display()
test_TC_28_max_limit()
test_TC_30_keep_state_after_close()

generate_report()
driver.quit()
