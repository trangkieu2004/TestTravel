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
    container = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"(//span[@role='combobox'])[ {container_index} ]")
    ))
    container.click()
    time.sleep(1)

    items = wait.until(lambda d: d.find_elements(
        By.XPATH, "//body//ul[contains(@class,'select2-results__options')]/li[contains(@class,'select2-results__option')]"
    ))

    countries = []
    for li in items:
        name = li.text.strip()
        li_id = li.get_attribute("id")
        if name and li_id:
            code = li_id.split('-')[-1].lower()
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
    time.sleep(1)
    return name, code

# ================== ENTER DATE ==================
def enter_travel_date(date_str="04-12-2025"):
    print(f"📅 Nhập ngày đi: {date_str}")
    date_input = wait.until(EC.presence_of_element_located((By.ID, "date")))
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
    date_input.clear()
    date_input.send_keys(date_str)
    print("✅ Ngày đã nhập.\n")

# ================== SUBMIT VISA SEARCH ==================
def click_search():
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    submit_button.click()
    wait.until(EC.url_contains("/visa/submit/"))
    print("✅ Đã vào Submission Form page\n")

# ================== FILL SUBMISSION FORM ==================
def fill_submission_form(first_name, last_name, email, phone):
    print("📝 Điền thông tin khách hàng...")
    
    # Trường First Name
    wait.until(EC.presence_of_element_located((By.NAME, "first_name"))).send_keys(first_name)
    
    # Trường Last Name
    driver.find_element(By.NAME, "last_name").send_keys(last_name)
    
    # Trường Email
    driver.find_element(By.NAME, "email").send_keys(email)
    
    # Trường Phone
    driver.find_element(By.NAME, "phone").send_keys(phone)
    
    print("✅ Thông tin đã điền.\n")


def submit_submission_form():
    # Nhấn nút Submit bằng ID
    wait.until(EC.element_to_be_clickable((By.ID, "submit"))).click()
    print("✅ Submit form thành công.\n")


# ================== FLOW ==================
try:
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

    # Nhấn Search → vào Submission Form
    click_search()

    # Điền thông tin khách hàng
    fill_submission_form(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="0123456789"
    )

    # Submit form
    submit_submission_form()

finally:
    driver.quit()
