import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from browsermobproxy import Server

def get_headless_driver(no_sandbox=False):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if no_sandbox:
        chrome_options.add_argument('--no-sandbox')
    current_path = os.path.dirname(__file__)
    filename = os.path.join(current_path, 'chromedriver')
    driver = webdriver.Chrome(filename, chrome_options=chrome_options)
    # driver.fram
    return driver


def get_headed_driver():
    current_path = os.path.dirname(__file__)
    filename = os.path.join(current_path, 'chromedriver')
    driver = webdriver.Chrome(filename)

    return driver

# def get_headed_proxy():
#     server = Server('browsermob-proxy-2.1.4/bin/browsermob-proxy')
#     server.start()
#     proxy = server.create_proxy()
#
#     current_path = os.path.dirname(__file__)
#     filename = os.path.join(current_path, 'chromedriver')
#
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
#     browser = webdriver.Chrome(filename, chrome_options=chrome_options)
#     return proxy, browser

def wait_for_xpath(driver, xpath, time=10):
    element = WebDriverWait(driver, time).until(  # wait for form
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return element


def wait_for_tag(driver, tag, time=10):
    element = WebDriverWait(driver, time).until(  # wait for form
        EC.presence_of_element_located((By.TAG_NAME, tag))
    )
    return element


def wait_for_classname(driver, classname, time=10):
    element = WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.CLASS_NAME, classname))
    )
    return element


def wait_for_id(driver, id, time=10):
    element = WebDriverWait(driver, time).until(
        EC.presence_of_element_located((By.ID, id))
    )
    return element


def wait_for_visible_id(driver, id, time=10):
    element = WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.ID, id))
    )
    return element

def wait_for_invisible_id(driver, id, time=10):
    return WebDriverWait(driver, time).until(
        EC.invisibility_of_element_located((By.ID, id))
    )

def wait_for_invisible_class_name(driver, classname, time=10):
    return WebDriverWait(driver, time).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, classname))
    )

def wait_for_visible_xpath(driver, xpath, time=10):
    element = WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    return element

def wait_for_clickable_xpath(driver, xpath, time=10):
    element = WebDriverWait(driver, time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    return element


def get_selenium_xpath_if_exists(driver, xpath):
    if len(driver.find_elements_by_xpath(xpath)) < 1:
        return ''
    text = driver.find_element_by_xpath(xpath) if 'text' in xpath else driver.find_element_by_xpath(xpath).text
    return text.strip() if text else ''

def wait_for_alert(driver, time=10):
    WebDriverWait(driver, time).until(
        EC.alert_is_present()
    )







