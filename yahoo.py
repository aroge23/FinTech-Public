import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import lxml.html

prices = []
names = []
changes = []
percentChanges = []
marketCaps = []
totalVolumes = []
circulatingSupplys = []

url = "https://in.finance.yahoo.com/quote/AAPL"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, features="lxml")

for i in range(40, 404, 14):
    for row in soup.find_all('tbody'):
        for srow in row.find_all('tr'):
            for name in srow.find_all('td', attrs={'class': 'data-col1'}):
                names.append(name.text)
            for price in srow.find_all('td', attrs={'class': 'data-col2'}):
                prices.append(price.text)
            for change in srow.find_all('td', attrs={'class': 'data-col3'}):
                changes.append(change.text)
            for percentChange in srow.find_all('td', attrs={'class': 'data-col4'}):
                percentChanges.append(percentChange.text)
            for volume in srow.find_all('td', attrs={'class': 'data-col5'}):
                totalVolumes.append(volume.text)

# url = "https://store.steampowered.com/explore/new/"
html = requests.get(url)
doc = lxml.html.fromstring(html.content)
new_releases = doc.xpath('//table[@class="W(100%)"]')[0]
titles = new_releases.xpath('.//span[@data-reactid="13"]/text()')
# name = titles.xpath('.//span[@data-reactid="96"]')
# titles = new_releases.xpath('.//span[@class="Trsdu(0.3s) "]/text()')
# new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]
# titles = new_releases.xpath('.//span[@class="top_tag"]/text()')

print(titles)
#print(pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Volume" : totalVolumes}))