import requests
import lxml.html
import re
import datetime

start_date = "2017-02-14"
sYear, sMonth, sDay = int(start_date.split("-")[0]), int(start_date.split("-")[1]), int(start_date.split("-")[2])
end_date = datetime.datetime.today().strftime("20%y-%m-%d")
eYear, eMonth, eDay = int(end_date.split("-")[0]), int(end_date.split("-")[1]), int(end_date.split("-")[2])
yearlist, twoyield, tenyield = [], [], []
first = ""

for i in range(sYear, eYear + 1):
    url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year=" + str(i)

    html = requests.get(url)
    global doc
    doc = lxml.html.fromstring(html.content)
    table = doc.xpath('//table[@class="t-chart"]')[0]
    oddrow = table.xpath('.//tr[@class="oddrow"]')
    evenrow = table.xpath('.//tr[@class="evenrow"]')

    i = 0
    while i < len(evenrow):
        if evenrow[i].xpath('.//td[@scope="row"]/text()')[0].split("/") == [start_date.split("-")[1], start_date.split("-")[2], start_date.split("-")[0][2:]]:
            evenrow = evenrow[i:]
            oddrow = oddrow[i:]
            first = "even"
            break
        if oddrow[i].xpath('.//td[@scope="row"]/text()')[0].split("/") == [start_date.split("-")[1], start_date.split("-")[2], start_date.split("-")[0][2:]]:
            evenrow = evenrow[i:]
            oddrow = oddrow[i:]
            first = "odd"
            break
        i += 1

    i = 0
    while i < len(oddrow):
        if first == "odd":
            yearlist.append(oddrow[i].xpath('.//td[@scope="row"]/text()')[0])
            row = oddrow[i].xpath('.//td[@class="text_view_data"]')
            twoyield.append(row[6].xpath('./text()')[0])
            tenyield.append(row[10].xpath('./text()')[0])

        if (len(oddrow) > len(evenrow)) and i == (len(oddrow) - 1):
            break

        yearlist.append(evenrow[i].xpath('.//td[@scope="row"]/text()')[0])
        row = evenrow[i].xpath('.//td[@class="text_view_data"]')
        twoyield.append(row[6].xpath('./text()')[0])
        tenyield.append(row[10].xpath('./text()')[0])
        first = "odd"

        i += 1

for i in range(len(doc.xpath('//script[@type="text/javascript"]'))):
    if doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()'):
        if doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0].find(
                ".parent().remove()") != -1:
            twoyield.remove(twoyield[yearlist.index(doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0][75:83])])
            tenyield.remove(tenyield[yearlist.index(doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0][75:83])])
            yearlist.remove(doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0][75:83])

numList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(len(twoyield) - 1):
    if twoyield[i][0] not in numList:
        yearlist.remove(yearlist[i])
        twoyield.remove(twoyield[i])
        tenyield.remove(tenyield[i])
        i -= 1

tenyield = [float(re.search(r'\d+.\d+', number).group()) for number in tenyield]
twoyield = [float(re.search(r'\d+.\d+', number).group()) for number in twoyield]

yinv = []
for i in range(len(tenyield)):
    yinv.append(tenyield[i] - twoyield[i])

print(yearlist)
print(len(tenyield))
print(len(twoyield))
print(yearlist[42])



# with open(tick.upper() + '.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow([" ", datetime.datetime.today().strftime("%e-%b-%Y")])
#     for i in range(len(titles)):
#         writer.writerow([titles[i], values[i]])
#
# csv_input = pd.read_csv(tick.upper() + '.csv')
# # for i in range(len(values)):
# #     csv_input['today'] = values[i]
# # csv_input.to_csv(tick.upper() + '.csv', index=False)
#
# # # read in the data from file
# # csv_input[datetime.datetime.today().strftime("%e-%b-%y") + 'test'] = values[0]
# # csv_input.to_csv(tick.upper() + '.csv', index=False)
#
# default_text = 'Some Text'
# # Open the input_file in read mode and output_file in write mode
# with open(tick.upper() + '.csv', 'r') as read_obj, \
#         open('output_1.csv', 'w', newline='') as write_obj:
#     # Create a csv.reader object from the input file object
#     csv_reader = csv.reader(read_obj)
#     # Create a csv.writer object from the output file object
#     csv_writer = csv.writer(write_obj)
#     # Read each row of the input csv file as list
#     for row in csv_reader:
#         # Append the default text in the row / list
#         row.append(default_text)
#         # Add the updated row / list to the output file
#         csv_writer.writerow(row)
#
# data = [line for line in csv.reader('output_1.csv')]
# # for i in range(len(values)):
# #     data[i + 1][len(data[0])] = values[i]
# # write the file back
# csv.writer(open(tick.upper() + '.csv', 'w')).writerows(data)