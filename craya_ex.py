import os
import sys
import requests
import re
import time
import json
import pandas as pd
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import warnings
warnings.filterwarnings('ignore')

extracts = re.compile('[^ 가-힣|a-z|A-Z|0-9|\[|\]|(|)|-|~|?|!|.|,|:|;|%]+')

nowDatetime = datetime.now().strftime('%Y-%m-%d')  # 날짜 표기를 위함

data_url_path = f'./data_ya/yanolja_busan[{nowDatetime}].csv'
data_path = f'./data_ya/info_yanolja_busan[{nowDatetime}].csv'
data_r_path = f'./reviews_ya/reviews_busan[{nowDatetime}].csv'

def scrape_website():
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get('https://www.yanolja.com/motel/r-910047?lat=37.50681&lng=127.06624&advert=AREA&topAdvertiseMore=0&sort=133&placeListType=motel&pathDivision=r-910047')

        with open(data_path, 'w', encoding='utf8', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(['name', 'basic_info'])

            for i in range(1, 100):
                try:
                    for _ in range(3):
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                        time.sleep(1)

                    xpath = f'//*[@id="__next"]/div[2]/section[2]/div/div/div[{i}]'
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    element.click()
                    time.sleep(3)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    tarname = soup.select('#__next > div > div > main > article > div:nth-child(1) > div.css-40tgm5')
                    rname = soup.find("div", {"class": "css-jyf8pg"})
                    name = rname.find("div", {"class": "property-title css-fie5xt"}).text.strip()

                    tarbasic_info = soup.select('#__next > div > div > main > article > div:nth-child(2) > div > div.css-17c0wg8')
                    basic_info = ' '.join([text.getText().strip() for text in tarbasic_info])
                    basic_info = extracts.sub('', basic_info)
                    basic_info = re.sub(' +', ' ', basic_info)

                    csv_writer.writerow([name, basic_info])

                    driver.back()
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    continue

        print("Scraping completed successfully.")

scrape_website()