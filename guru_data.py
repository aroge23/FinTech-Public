import lxml.html as web
import pandas as pd
import requests
from selenium import webdriver
import time


def getGuruPortfolios(numOfGurus):
    url = 'https://www.gurufocus.com/guru/portfolio'

    html = requests.get(url)
    doc = web.fromstring(html.content)
    all_data = {}
    gurus = doc.xpath('//td[@data-column="Guru Name"]')
    guru_names = []

    for i in range(len(gurus) - (40 - numOfGurus)):
        guru_names.append(gurus[i].xpath('.//a[@class="guru-router-link"]/text()')[0][1:])
        browser = webdriver.Chrome('/Users/anay-mac/Downloads/chromedriver')
        browser.get('https://www.gurufocus.com/guru/portfolio')

        user = browser.find_elements_by_xpath('//a[@class="guru-router-link el-popover__reference"]')
        user[i].click()
        time.sleep(2)
        user = browser.find_elements_by_xpath('//a[@class="guru-menu-item"]')
        user[1].click()
        time.sleep(2)

        names = []
        next = browser.find_element_by_class_name('btn-next')
        length = browser.find_elements_by_class_name('number')
        length = int(length[len(length) - 1].text)

        for k in range(length):
            bnames = browser.find_elements_by_xpath('//td[@class="table-company_name-info"]')
            for j in range(len(bnames)):
                names.append([bnames[j].text])
                if browser.find_elements_by_xpath('//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(j) + ']/td[9]/span[1]') != []:
                    print(browser.find_elements_by_xpath('//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(j) + ']/td[9]/span[1]')[0].text)
            next.click()
            time.sleep(1)

        browser.quit()
        all_data[guru_names[i]] = names

    return pd.DataFrame({tic : pd.Series(rev) for tic, rev in all_data.items()})

def getGuruTop10():
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
        names.append(browser.find_elements_by_xpath(
            '//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[1]/span[1]')[0])
        temp = []
        for obj in browser.find_elements_by_xpath(
                '//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[4]/div')[1:]:
            temp.append(obj.text.split('\n'))
        all_data[names[i - 1]] = temp

    next.click()
    time.sleep(2)

    for i in range(1, 28):
        names.append(browser.find_elements_by_xpath(
            '//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[1]/span[1]')[0].text)
        temp = []
        for obj in browser.find_elements_by_xpath(
                '//table[@class="data-table normal-table"]/tbody[1]/tr[' + str(i) + ']/td[4]/div')[1:]:
            temp.append(obj.text.split('\n'))
        all_data[names[40 + (i - 1)]] = temp

    browser.quit()
    return pd.DataFrame({tic: pd.Series(rev, dtype='object') for tic, rev in all_data.items()})

print(getGuruPortfolios(2))