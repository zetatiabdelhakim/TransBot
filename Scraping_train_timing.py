# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.oncf.ma/fr/")
gare_depart = "TANGER"
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
    time.sleep(2)
    date_to_scrape = "20/07/2024"
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
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-btn.css-osurd.ant-btn-round.ant-btn-default.btn-primary"))
    )[1].click()
    time.sleep(5)
    # title  ["depart", "arrive", "date_depart", "date_arrive", "prix", "dure", "trajet"] "18:00 - gare - 18:30 > 19:00 - gare"

    down_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".anticon.anticon-down"))
    )
    for b in down_buttons[:-1:2]:
        b.click()
        time.sleep(3)

    trains = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-col.ant-col-24.trips-wrapper"))
    )
    print(f"Gare de départ : {gare_depart}")
    print(f"Gare d'arrivée : {gare_darrive} \n\n")
    for i, train in enumerate(trains):
        print(f"Train - {i} --------------------------------")
        durations = train.find_elements(By.CSS_SELECTOR, '.duration-label')
        trips = train.find_elements(By.CSS_SELECTOR, '.TripCardFooter_timeline_info_label')

        heure_depart = durations[0].text
        heure_arrivee = durations[-1].text
        print(f"Heure de départ : {heure_depart}")
        print(f"Heure d'arrivée : {heure_arrivee}")

        corr_i = 1

        for duration, trip in zip(durations[1:-1], trips[1:-1]):
            heures = duration.text.split('\n')
            heure_corr1, heure_corr2 = heures

            infos_trajet = trip.text.split('\n')
            gare_correspendance = infos_trajet[0]
            duree_corr = infos_trajet[2]
            print(f"correspondance {corr_i} : {heure_corr1} à {gare_correspendance} - correspondance {duree_corr} - départ {heure_corr2}")
            corr_i += 1
            

        price = train.find_elements(By.CSS_SELECTOR, 'label.price')
        print(f"price : {price[0].text}\n\n")

finally:
    driver.quit()

