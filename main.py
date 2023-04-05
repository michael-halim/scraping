from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

import time
import datetime
import re
import os 
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = current + os.sep + os.pardir
sys.path.append(parent_dir)

from helper_func.helper import print_help, replace_multiple_char, replace_text_in_between, replace_multiple_tags, save_to_file, get_today 

from dotenv import load_dotenv
load_dotenv()

SAVE_LOG_PATH = os.path.join(os.path.dirname(__file__), 'scraping_logs' + os.sep)
LOG_FILENAME = str(get_today()) + '.txt'

def get_contact(driver):
    pass
    # url = ''
    # driver.get(url)

    # phones = driver.find_elements(By.CSS_SELECTOR, 'td > a[href*="konsultasi"]')
    # addresses = driver.find_elements(By.CSS_SELECTOR, 'ul[data-identifyelement="650"] > li[dir="ltr"]')

    # for phone, address in zip(phones, addresses):
    #     tmp_phone = phone.get_attribute('innerHTML')
    #     tmp_address = address.get_attribute('innerHTML')

def get_every_product(driver, phone, address):
    pass 

def get_every_detail(driver):
    pass

def main():
    # https://chromedriver.storage.googleapis.com/index.html
    s = Service(os.environ.get('CHROMEDRIVER_PATH_DEVELOPMENT'))
    if os.environ.get('DEVELOPMENT_MODE') == 'False':
        s = Service(os.environ.get('CHROMEDRIVER_PATH_PRODUCTION'))

    options = Options()

    if os.environ.get('DEVELOPMENT_MODE') == 'False':
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(service=s, options=options)

    driver.implicitly_wait(15)

    start_time = time.perf_counter()
    print_help(var='RUNNING WEBSITE SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    
    phone, address = get_contact(driver=driver)
    get_every_product(driver=driver, phone=phone, address=address)
    get_every_detail(driver=driver)

    driver.quit()
    
    print_help(var='FINISHED WEBSITE SCRAPING....', username='MAIN', save_log_path=SAVE_LOG_PATH, log_filename=LOG_FILENAME)
    print('--- %s ---' % (datetime.timedelta(seconds = time.perf_counter() - start_time)))

if __name__ == '__main__':
    main()