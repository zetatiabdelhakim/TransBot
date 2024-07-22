from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from collections import defaultdict


# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.oncf.ma/fr/")
gare_depart = "TANGER"
date_to_scrape = "20/07/2024"

gare_darrive = "AGADIR (SUPRAT.)"

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

    # time.sleep(1)

    li_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#ui-id-1 > li"))
    )

    for li in li_elements:
        if gare_depart in li.text:
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

    # time.sleep(1)

    li_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#ui-id-2 > li"))
    )

    for li in li_elements:
        if gare_darrive in li.text:
            li.click()
            break

    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.first-tab.formValidate"))
    )
    # time.sleep(2)
    form.submit()
    # time.sleep(2)
    next_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.button.button-uppercase"))
    )

    driver.execute_script("arguments[0].target = '_self';", next_page)

    next_page.click()
    # time.sleep(1)

    date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.ant-input"))
    )

    date.click()
    time.sleep(1)
    # we are assuming that we are scraping the current month or the next one
    now = datetime.now()
    current_month = now.month
    date_to_scrape_month = int(date_to_scrape.split("/")[1])
    if date_to_scrape_month != current_month:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".react-datepicker__navigation.react-datepicker__navigation--next"))
        ).click()

    the_day = int(date_to_scrape.split("/")[0])
    days = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".react-datepicker__day"))
    )
    begin = False
    for i in days :
        if int(i.text) == 1:
            begin = True
        if begin and int(i.text) == the_day:
            i.click()
            break

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".ant-btn.css-osurd.ant-btn-primary.DatePickerModal_confirm"))
    ).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-btn.css-osurd.ant-btn-round.ant-btn-default.btn-primary"))
    )[1].click()
    time.sleep(1)
    # title  ["depart", "arrive", "date_depart", "date_arrive", "prix", "dure", "trajet"] "18:00 - gare - 18:30 > 19:00 - gare"

    print(f"Date : {date_to_scrape}")
    print(f"Gare de départ : {gare_depart}")
    print(f"Gare d'arrivée : {gare_darrive} \n\n")

    visited = defaultdict(bool)
    some_thing_new = True
    count = 1
    while some_thing_new:
        some_thing_new = False

        down_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".anticon.anticon-down"))
        )
        for b in down_buttons[:-1:2]:
            b.click()
            time.sleep(1)

        trains = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-col.ant-col-24.trips-wrapper"))
        )

        for i, train in enumerate(trains):
            durations = train.find_elements(By.CSS_SELECTOR, '.duration-label')
            trips = train.find_elements(By.CSS_SELECTOR, '.TripCardFooter_timeline_info_label')

            if visited[durations[0].text]:
                continue
            else:
                visited[durations[0].text] = True
                some_thing_new = True

            print(f"Train - {count} --------------------------------")
            correspondances = []
            count += 1
            heure_depart = durations[0].text
            heure_arrivee = durations[-1].text

            corr_i = 1

            for duration, trip in zip(durations[1:-1], trips[1:-1]):
                heures = duration.text.split('\n')
                heure_corr1, heure_corr2 = heures

                infos_trajet = trip.text.split('\n')
                gare_correspendance = infos_trajet[0]
                duree_corr = infos_trajet[2]
                correspondance = f"correspondance {corr_i} : {heure_corr1} à {gare_correspendance} - correspondance {duree_corr} - départ {heure_corr2}"
                correspondances.append(correspondance)


            price = train.find_elements(By.CSS_SELECTOR, 'label.price')[0].text

            print(correspondances)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".CustomLink--default.trip-cta-next-trains"))
        ).click()
        time.sleep(1)


finally:
    driver.quit()

