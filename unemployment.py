import traceback
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
from pyscraper.selenium_utils import get_headed_driver, get_headless_driver, wait_for_xpath, wait_for_clickable_xpath, \
    wait_for_invisible_class_name, wait_for_invisible_id
import sqlite3


def wait_masks(driver):
    time.sleep(.5)
    wait_for_invisible_id(driver, 'FilterHdrPanel_mask', time=20)
    wait_for_invisible_id(driver, "filterHdr_wait_mask", time=20)
    wait_for_invisible_class_name(driver, 'mask', time=20)


conn = sqlite3.connect('factfinder.db')
cur = conn.cursor()
# cur.execute('CREATE TABLE UNEMPLOYMENT (name TEXT, population INT, employment TEXT, unemployment TEXT)')


def modify_table(driver):
    add_geographies = wait_for_clickable_xpath(driver, '//*[@id="addRemoveGeo_btn"]')
    add_geographies.click()
    wait_masks(driver)
    geo_type = wait_for_clickable_xpath(driver, '//*[@id="summaryLevel"]')
    geo_type.click()
    geo_type.find_element_by_xpath('./option[@value="160"]').click()
    wait_masks(driver)
    all_places = wait_for_clickable_xpath(driver, '//*[@id="geoAssistList"]/option[1]')
    all_places.click()
    add_button = wait_for_clickable_xpath(driver, '//*[@id="addtoyourselections"]')
    add_button.click()
    wait_masks(driver)
    show_table = wait_for_clickable_xpath(driver, '//*[@id="showTableBtn"]')
    show_table.click()
    wait_masks(driver)

    driver.execute_script('toggleTT()')
    wait_masks(driver)
    types_filter = wait_for_clickable_xpath(driver, '//*[@id="data"]/thead/tr[2]/th[1]/a')
    types_filter.click()
    total = wait_for_clickable_xpath(driver, '//*[@id="c_HC01"]')
    total.click()
    employment = wait_for_clickable_xpath(driver, '//*[@id="c_HC03"]')
    employment.click()
    unemployment = wait_for_clickable_xpath(driver, '//*[@id="c_HC04"]')
    unemployment.click()
    ok_button = wait_for_clickable_xpath(driver, '//*[@id="yui-gen4-button"]')
    ok_button.click()

    wait_masks(driver)
    result_filter = wait_for_clickable_xpath(driver, '//*[@id="data"]/thead/tr[3]/th[1]/a')
    result_filter.click()
    estimate = wait_for_clickable_xpath(driver, '//*[@id="c_EST"]')
    estimate.click()
    ok_button = wait_for_clickable_xpath(driver, '//*[@id="yui-gen4-button"]')
    ok_button.click()
    wait_masks(driver)
    driver.execute_script('toggleTT()')


def extract_values(driver):
    total_names = []
    loop = True
    # stack = []
    while loop:
        try:
            wait_masks(driver)
            headers = [element.text for element in driver.find_elements_by_xpath('//*[@id="data"]/thead/tr[1]/th')][1:]
            names = []

            if any(header in total_names for header in headers):
                driver.execute_script("stepshift('h', 'f')")
                continue

            for header in headers:
                names.append(header)
                names.append(header)
                names.append(header)

            if not loop:
                break
            wait_masks(driver)
            population = []

            try:
                population = [el.text for el in driver.find_elements_by_xpath('//*[@id="data"]/tbody/tr[1]/td')]
            except:
                traceback.print_exc()
                print()

            if len(names) == 0:
                continue

            for i in range(0, len(population), 3):
                try:
                    n = names[i]
                    place_population = int(population[i].replace(',', ''))
                    employment_ratio = population[i + 1]
                    unemployment_ratio = population[i + 2]
                    print(n, place_population, employment_ratio, unemployment_ratio)
                    cur.execute('INSERT INTO UNEMPLOYMENT VALUES(?, ?, ?, ?)', (n, place_population, employment_ratio, unemployment_ratio))
                    conn.commit()
                except:
                    traceback.print_exc()
                    print('')

            for header in headers:
                total_names.append(header)
            driver.execute_script("stepshift('h', 'f')")
            time.sleep(1)
        except:
            traceback.print_exc()
            print()


driver = get_headless_driver(no_sandbox=True)
driver.get(
    'https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=ACS_16_5YR_S2301&prodType=table')
modify_table(driver)
extract_values(driver)
