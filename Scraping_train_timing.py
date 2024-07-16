from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.oncf.ma/fr/")

try:
    div_inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#complete"))
    )
    div_inputs[0].click()

    comp_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "autocomplete"))
    )

    comp_input.send_keys("c")
    comp_input.send_keys(Keys.BACKSPACE)

    time.sleep(1)

    li_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#ui-id-1 > li"))
    )

    for li in li_elements:
        if "SETTAT" in li.text:
            li.click()
            break
    """
    -------------------------------------------------------------- the second input
    """

    div_inputs[1].click()

    comp_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "autocomplete2"))
    )

    # Send the key 'c' and then delete it
    comp_input.send_keys("c")
    comp_input.send_keys(Keys.BACKSPACE)

    time.sleep(1)

    li_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#ui-id-2 > li"))
    )

    for li in li_elements:
        if "CASA PORT" in li.text:
            li.click()
            break

    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.first-tab.formValidate"))
    )
    time.sleep(2)
    form.submit()
    time.sleep(2)
    next_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.button.button-uppercase"))
    )

    next_page.click()
    time.sleep(5)

finally:
    driver.quit()
