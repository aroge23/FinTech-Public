#PULLS DATA FROM YAHOO FINANCE AND WRITES TO A CSV FILE
import requests
import lxml.html
import csv
import pandas as pd
import datetime

tick = "wday"

url = "https://in.finance.yahoo.com/quote/" + tick.upper()

html = requests.get(url)
doc = lxml.html.fromstring(html.content)
left_summary = doc.xpath('//div[@data-test="left-summary-table"]')[0]
td = left_summary.xpath('.//td[@class="C($primaryColor) W(51%)"]')
titles = []
values = []
for element in td:
    titles.append(element.xpath('.//span/text()')[0])
td = left_summary.xpath('.//td[@class="Ta(end) Fw(600) Lh(14px)"]')
for element in td:
    if len(element.xpath('.//span/text()')) != 0:
        values.append(element.xpath('.//span/text()')[0])
    else:
        values.append(element.xpath('./text()')[0])

right_summary = doc.xpath('//div[@data-test="right-summary-table"]')[0]
td = right_summary.xpath('.//td[@class="Ta(end) Fw(600) Lh(14px)"]')
for element in td:
    if len(element.xpath('.//span/text()')) != 0:
        values.append(element.xpath('.//span/text()')[0])
    else:
        values.append(element.xpath('./text()')[0])

td = right_summary.xpath('.//td[@class="C($primaryColor) W(51%)"]')
for element in td:
    titles.append(element.xpath('.//span/text()')[0])


with open(tick.upper() + '.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([" ", datetime.datetime.today().strftime("%e-%b-%Y")])
    for i in range(len(titles)):
        writer.writerow([titles[i], values[i]])

csv_input = pd.read_csv(tick.upper() + '.csv')
# for i in range(len(values)):
#     csv_input['today'] = values[i]
# csv_input.to_csv(tick.upper() + '.csv', index=False)

# # read in the data from file
# csv_input[datetime.datetime.today().strftime("%e-%b-%y") + 'test'] = values[0]
# csv_input.to_csv(tick.upper() + '.csv', index=False)

default_text = 'Some Text'
# Open the input_file in read mode and output_file in write mode
with open(tick.upper() + '.csv', 'r') as read_obj, \
        open('output_1.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = csv.reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = csv.writer(write_obj)
    # Read each row of the input csv file as list
    for row in csv_reader:
        # Append the default text in the row / list
        row.append(default_text)
        # Add the updated row / list to the output file
        csv_writer.writerow(row)

data = [line for line in csv.reader('output_1.csv')]
# for i in range(len(values)):
#     data[i + 1][len(data[0])] = values[i]
# write the file back
csv.writer(open(tick.upper() + '.csv', 'w')).writerows(data)

print(titles)
print(values)
print(data)

#print(pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Volume" : totalVolumes}))