import requests
import lxml.html
import re

year = "2010"

url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year=" + year

html = requests.get(url)
doc = lxml.html.fromstring(html.content)
table = doc.xpath('//table[@class="t-chart"]')[0]
oddrow = table.xpath('.//tr[@class="oddrow"]')
evenrow = table.xpath('.//tr[@class="evenrow"]')

yearlist, twoyield, tenyield = [], [], []
i = 0
while i < len(oddrow):
    yearlist.append(oddrow[i].xpath('.//td[@scope="row"]/text()')[0])
    row = oddrow[i].xpath('.//td[@class="text_view_data"]')
    twoyield.append(row[6].xpath('./text()')[0])
    tenyield.append(row[10].xpath('./text()')[0])

    if (len(oddrow) > len(evenrow)) and i == (len(oddrow) - 1):
        print("test")
        break

    yearlist.append(evenrow[i].xpath('.//td[@scope="row"]/text()')[0])
    row = evenrow[i].xpath('.//td[@class="text_view_data"]')
    twoyield.append(row[6].xpath('./text()')[0])
    tenyield.append(row[10].xpath('./text()')[0])

    i += 1

numList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(len(twoyield) - 1):
    if twoyield[i][0] not in numList:
        yearlist.remove(yearlist[i])
        twoyield.remove(twoyield[i])
        tenyield.remove(tenyield[i])
        i -= 1

tenyield = [float(re.search(r'\d+.\d+', number).group()) for number in tenyield]
twoyield = [float(re.search(r'\d+.\d+', number).group()) for number in twoyield]

print(len(yearlist))
print(len(tenyield))
print(len(twoyield))