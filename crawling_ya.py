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
from selenium.webdriver.common.action_chains import ActionChains

import warnings
warnings.filterwarnings('ignore')

extracts = re.compile('[^ 가-힣|a-z|A-Z|0-9|\[|\]|(|)|-|~|?|!|.|,|:|;|%]+')

nowDatetime = datetime.now().strftime('%Y-%m-%d') # 날짜 표기를 위함

data_url = open('./data_ya/yanolja_busan[' + nowDatetime +'].csv', 'w', encoding='utf8')
data = open('./data_ya/info_yanolja_busan[' + nowDatetime +'].csv', 'w', encoding='utf8')
data_r = open('./reviews_ya/reviews_busan[' + nowDatetime +'].csv' , 'w', encoding='utf8')

driver = webdriver.Chrome("chromedriver.exe")
Url = 'https://www.yanolja.com/motel/r-910047?lat=37.50681&lng=127.06624&advert=AREA&topAdvertiseMore=0&sort=133&placeListType=motel&pathDivision=r-910047'
driver.get(Url)
# driver.maximize_window()

data.write('"name"')
data.write(", ")
data.write('"basic_info"')
data.write(", ")
# data.write('"cost_info"')
# data.write(", ")
data.write('"avg_stars"')
data.write("\n")

for i in range(1, 100):
    try:
        xpath = '/html/body/div[1]/div[2]/section[2]/div/div/div[{}]'.format(i)
        print(xpath)
        element = driver.find_element(By.XPATH, xpath)

        # 클릭 가능한 영역으로 스크롤링
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()
        time.sleep(1)

        # 클릭
        element.click()
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        tarname = soup.select('#__next > div > div > main > article > div:nth-child(1) > div.css-40tgm5')
        rname = soup.find("div", {"class" : "css-jyf8pg"})
        name = rname.find("div", {"class":"property-title css-fie5xt"})
        name = name.text

        tarbasic_info = soup.select('#__next > div > div > main > article > div:nth-child(2) > div > div.css-17c0wg8')
        basic_info = ''
        for text in tarbasic_info:
            basic_info += text.getText()

        basic_info = extracts.sub('', basic_info)
        basic_info = re.sub(' +', ' ', basic_info)
        basic_info = '"'+basic_info+'"'

        tarstar_info = soup.select('#__next > div > div > main > article > div:nth-child(1) > div.css-40tgm5 > div.css-84qvow')
        avg_star_info = tarstar_info.find("span").text


        data.write(name)
        data.write(', ')
        data.write(basic_info)
        data.write(', ')
        data.write(avg_star_info)
        data.write('\n')

        driver.back()
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    except Exception as e:
        print(f"Error occured at index {i} : {str(e)}")
        continue

data.close()
driver.close()