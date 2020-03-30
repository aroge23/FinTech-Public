#PULLS DATA FROM YAHOO FINANCE AND WRITES TO A CSV FILE
import requests
import lxml.html

url = "https://in.finance.yahoo.com/quote/NKE"

# url = "https://store.steampowered.com/explore/new/"
html = requests.get(url)
doc = lxml.html.fromstring(html.content)
left_summary = doc.xpath('//div[@data-test="left-summary-table"]')[0]
titles = []
for number in [13, 18, 23, 28, 33, 37, 41, 46]:
    titles.append(left_summary.xpath('.//span[@data-reactid="' + str(number) + '"]/text()')[0])
values = left_summary.xpath('.//span[@class="Trsdu(0.3s) "]/text()')

right_summary = doc.xpath('//div[@data-test="right-summary-table"]')[0]
for number in [54, 59, 64, 69, 74, 81, 85, 90]:
    titles.append(right_summary.xpath('.//span[@data-reactid="' + str(number) + '"]/text()')[0])
values.append(right_summary.xpath('.//span[@class="Trsdu(0.3s) "]/text()'))


print(values)
#print(pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Volume" : totalVolumes}))