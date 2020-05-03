import requests as req
import lxml.html as web
import re
import datetime
from bs4 import BeautifulSoup
import html5lib
import mechanicalsoup as ms
import pandas as pd
import pandas_datareader as pdd
import datetime
from selenium import webdriver
import time

all_data = {}
names = []
browser = webdriver.Chrome('/Users/anay-mac/Downloads/chromedriver')
browser.get('https://www.gurufocus.com/guru/top-holdings')
next = browser.find_element_by_class_name('btn-next')
next.click()
time.sleep(2)
prev = browser.find_element_by_class_name('btn-prev')
prev.click()
time.sleep(2)
for i in range(1, 41):
     names.append(browser.find_elements_by_xpath('//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[1]/span[1]')[0].text)
     temp = []
     for obj in browser.find_elements_by_xpath('//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[4]/div')[1:]:
         temp.append(obj.text.split('\n'))
     all_data[names[i-1]] = temp
next.click()
time.sleep(2)
for i in range(1, 28):
     names.append(browser.find_elements_by_xpath('//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[1]/span[1]')[0].text)
     temp = []
     for obj in browser.find_elements_by_xpath('//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[4]/div')[1:]:
         temp.append(obj.text.split('\n'))
     all_data[names[40 + (i-1)]] = temp
browser.quit()
print(pd.DataFrame({tic : pd.Series(rev) for tic, rev in all_data.items()}))



# browser = ms.StatefulBrowser()
# browser.open('https://dvhs.schoolloop.com/portal/login')
# browser.select_form('form[action="/portal/login?etarget=login_form"]')
# browser['login_name'] = 'anayroge23'
# browser['password'] = 'anshanay2823'
# browser.submit_selected()
#
# browser.open('https://dvhs.schoolloop.com/loopmail/redirectMail')
# print(browser.get_url())
#
# doc = lxml.html.fromstring(str(browser.get_current_page()))
