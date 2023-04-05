from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import time
import datetime
import re
import os 
import urllib.request
import sys
import pandas as pd
import json

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = current + os.sep + os.pardir
sys.path.append(parent_dir)

from helper_func.helper import *

from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

class Scraping(webdriver.Chrome):

    dataset = []

    def __init__(self):
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

        super(Scraping, self).__init__(options=options, service=s)

        self.implicitly_wait(15)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def open_website(self, url):
        self.get(url)

    def scroll_untill_bottom(self):
        SCROLL_PAUSE_TIME = 0.5
        INCREASE_HEIGHT = 450

        # Get scroll height
        last_height = self.execute_script("return document.body.scrollHeight")
        new_height = 100
        while True:
            # Scroll down to bottom
            self.execute_script("window.scrollTo(0," + str(new_height) + ");")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height += INCREASE_HEIGHT
            if new_height >= last_height:
                break
    def click_next_page(self):
        print('FIND NEXT PAGE')
        next_page = self.find_element(By.CSS_SELECTOR, 'ul.pagination > li.next > a.chevron')
        
        try:   
            print('RETURNING CLICK NEXT PAGE')
            print(next_page.get_attribute('href'))
            if next_page.get_attribute('href') is not None:
                return True, next_page.get_attribute('href')

            raise Exception
        
        except Exception as e: 
            print('EXCEPTION NEXT PAGE')
            return False, ''
        
    def scrape_front_page(self):
        html = self.page_source
        # with open('output.txt','w', encoding="utf-8") as f:
        #     f.write(html)

        soup = BeautifulSoup(html, 'html.parser')
        
        names = soup.select('table.cmc-table > tbody > tr > td > div > a.cmc-link > div > div > p')
        names = [x.get_text() for x in names]

        symbols = soup.select('table.cmc-table > tbody > tr > td > div > a.cmc-link > div > div > div > p')
        symbols = [x.get_text() for x in symbols]

        prices = soup.select('table.cmc-table > tbody > tr > td:nth-child(4) > div > a > span')
        prices = [x.get_text() for x in prices]

        market_caps_object = soup.select('table.cmc-table > tbody > tr > td:nth-child(8)')
        market_caps = []
        for m in market_caps_object:
            tmp = m.select('span.sc-edc9a476-1.gqomIJ')
            market_caps += ['-'] if tmp == [] else [tmp[0].get_text()]


        volumes_object = soup.select('table.cmc-table > tbody > tr > td:nth-child(9)')
        vol_24h_dollars, vol_24h_symbols = [], []
        for v in volumes_object:
            dollar = v.select('div > a > p')
            symbol = v.select('div > div > p')

            # Append dollar[0] and symbol[0] if their value is not []
            vol_24h_dollars.append('-' if dollar == [] else dollar[0].get_text())
            vol_24h_symbols.append('-' if symbol == [] else symbol[0].get_text())
                
        
        circ_supplies_object = soup.select('table.cmc-table > tbody > tr > td:nth-child(10)')
        circ_supplies = []
        for c in circ_supplies_object:
            circ = c.select('div > div > p')

            # Append circ[0] if their value is not []
            circ_supplies.append('-' if circ == [] else circ[0].get_text())


        price_1h_24h_7ds = soup.select('table.cmc-table > tbody > tr > td > span.sc-97d6d2ca-0')
        price_1h_24h_7ds = [x.get_text() for x in price_1h_24h_7ds]

        print(price_1h_24h_7ds)

        images = soup.select('table.cmc-table > tbody > tr > td > div > a > div > img')
        images = [x['src'] for x in images]

        # Download Images
        # for image, symbol in zip(images, symbols):
        #     urllib.request.urlretrieve(image, os.path.join(os.path.dirname(__file__), 'img' ,symbol.replace('*','') + '.jpg') )

        links = soup.select('table.cmc-table > tbody > tr > td > div[display=flex] > a')
        links = ['https://coinmarketcap.com' + str(x['href']) for x in links]
        
        for co, (name, symbol, price, marcap, vol_24_d, vol_24_s, circ_supply, image, link) in \
            enumerate(zip(names, symbols, prices, market_caps, vol_24h_dollars, vol_24h_symbols, circ_supplies, images, links)):

            crypto_1h, crypto_24h, crypto_7d = price_1h_24h_7ds[co * 3: (co * 3) + 3]

            crypto_1h = replace_multiple_tags(crypto_1h, '<span','>','')
            crypto_1h = replace_multiple_tags(crypto_1h, '</span','>','')
            crypto_24h = replace_multiple_tags(crypto_24h, '<span','>','')
            crypto_24h = replace_multiple_tags(crypto_24h, '</span','>','')
            crypto_7d = replace_multiple_tags(crypto_7d, '<span','>','')
            crypto_7d = replace_multiple_tags(crypto_7d, '</span','>','')

            dataset_object = {
                'name':name,
                'symbol':symbol,
                'price':price,
                'marcaps':marcap,
                'crypto_1h':crypto_1h, 
                'crypto_24h':crypto_24h, 
                'crypto_7d':crypto_7d,
                'vol_24_d':vol_24_d,
                'vol_24_s':vol_24_s,
                'circ_supply':circ_supply,
                'image':image,
                'link':link
            }
            print_help(var=dataset_object, title='DATASET OBJECT')
            self.dataset.append(dataset_object)

    def save_data_to_file(self, file_type=['PYTHON'], filename='front_page'):
        dirname = os.path.dirname(__file__)
        dest_path = os.path.join(dirname, 'files', filename)

        if 'PYTHON' in file_type:
            # Save Complete Dataset to front_page.py
            save_to_file(dest_path=dest_path, 
                            filename=filename, 
                            itemList = self.dataset,
                            save_mode='a')

        if 'JSON' in file_type:
            with open(dest_path + '.json', 'w') as f:
                json.dump(self.dataset, f)

        df = pd.DataFrame(data=self.dataset)

        if 'EXCEL' in file_type:            
            df.to_excel(dest_path + '.xlsx', index=False)

        if 'CSV' in file_type:
            df.to_csv(dest_path + '.csv',sep=',')
        
def main():
    try:
        start_time = start_timer()
        time_log = []

        with Scraping() as bot:
            url = 'https://coinmarketcap.com'

            while True:
                bot.open_website(url)
                bot.scroll_untill_bottom()
                bot.scrape_front_page()
                    
                is_continue, url = bot.click_next_page()
                if not is_continue:
                    break

            bot.save_data_to_file(file_type=['PYTHON', 'JSON', 'EXCEL', 'CSV'])

            time_log = end_timer(start_time=start_time, time_log=time_log, add_time_log=True, message='SAVING DATA')
            [ print(log) for log in time_log ]

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()