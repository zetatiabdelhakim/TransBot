from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
class State:
    def __init__(self, link: str = "https://www.oncf.ma/fr/",
                 selector_clickable_div: str = "#complete",
                 selector_input: str = "#autocomplete",
                 selector_list_of_states: str = "#ui-id-1 > li"):
        self.states = self.init_states(link, selector_clickable_div, selector_input, selector_list_of_states, False)

    def __str__(self):
        return str(self.states)

    def init_states(self, link: str,
                    selector_clickable_div: str,
                    selector_input: str,
                    selector_list_of_states: str,
                    save: bool):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get(link)
        result = []

        try:
            div_inputs = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_clickable_div))
            )
            div_inputs.click()

            comp_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_input))
            )

            comp_input.send_keys("c")
            comp_input.send_keys(Keys.BACKSPACE)

            time.sleep(1)

            li_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_list_of_states))
            )
            for li in li_elements:
                result.append(li.text)

            if save:
                pass
        finally:
            driver.quit()
            return result


if __name__ == "__main__":
    s = State()
    print(s)
