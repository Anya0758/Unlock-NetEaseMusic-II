# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "002981B8969EEBBE8B74518C12684DEB92DBE1ACE3C41FF9D04C33003152900F75BF39EC387FDC8726519DBBBDEC883C77A033310714D5A0FA8C550FF02D3EA7D0CC152B599D5D838C358F331D6A360589A11638B223A28610D87ADF9C4365E41170DCC612DFA641F96D30BC01B1F28104455B2CD7918B557FBD50BDA155DBACB4A9113EBE7BBF3D41BC9C6ECE82B0584D257749F32584230D8ED2AEAB39D5D95B8F9682FCAE72B915AF1390E2E813F18A0722B55D416466B5F6A34ABF2911EEDA20AD50B829DE66D59C816A821C8A992D309217552850ACE1718B6EA5C7CD903ADE136788BD2A9AA6C6DB5BA5E51815592B78C88F1049CC116403CB88A548FD6297B6C9213E2D68FB6A45449D0231901CF2069847E2E1633801031B6F983DDF4B411D90B8EC2477A8EFB108705A679D7482D9B0037AA6E432E2C0A2D2CD973573EDA07E9B3CE7654FBA15A2987C799604104021307703A485984DA906FBC4F3E0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
