import requests
import lxml.html
import re

def yieldInv(start_date, end_date):
    start_date = start_date
    sYear, sMonth, sDay = int(start_date.split("-")[0]), int(start_date.split("-")[1]), int(start_date.split("-")[2])
    end_date = end_date
    eYear, eMonth, eDay = int(end_date.split("-")[0]), int(end_date.split("-")[1]), int(end_date.split("-")[2])
    yearlist, twoyield, tenyield = [], [], []
    first = ""

    for i in range(sYear, eYear + 1):
        url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year=" + str(
            i)

        html = requests.get(url)
        global doc
        doc = lxml.html.fromstring(html.content)
        table = doc.xpath('//table[@class="t-chart"]')[0]
        oddrow = table.xpath('.//tr[@class="oddrow"]')
        evenrow = table.xpath('.//tr[@class="evenrow"]')

        i = 0
        while i < len(evenrow):
            if evenrow[i].xpath('.//td[@scope="row"]/text()')[0].split("/") == [start_date.split("-")[1],
                                                                                start_date.split("-")[2],
                                                                                start_date.split("-")[0][2:]]:
                evenrow = evenrow[i:]
                oddrow = oddrow[i:]
                first = "even"
                break
            if oddrow[i].xpath('.//td[@scope="row"]/text()')[0].split("/") == [start_date.split("-")[1],
                                                                               start_date.split("-")[2],
                                                                               start_date.split("-")[0][2:]]:
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

    #CHECKS IF THERE ARE ANY VALUES THAT ARE REMOVED BY THE HOST
    for i in range(len(doc.xpath('//script[@type="text/javascript"]'))):
        if doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()'):
            if doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0].find(".parent().remove()") != -1:
                twoyield.remove(twoyield[yearlist.index(
                    doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0][75:83])])
                tenyield.remove(tenyield[yearlist.index(
                    doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0][75:83])])
                yearlist.remove(doc.xpath('//script[@type="text/javascript"]')[i].xpath('./text()')[0][75:83])

    # GET RID OF NON-INTEGER VALUES
    numList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(len(twoyield) - 1):
        if twoyield[i][0] not in numList:
            yearlist.remove(yearlist[i])
            twoyield.remove(twoyield[i])
            tenyield.remove(tenyield[i])
            i -= 1

    # CONVERT STRINGS TO FLOATS
    tenyield = [float(re.search(r'\d+.\d+', number).group()) for number in tenyield]
    twoyield = [float(re.search(r'\d+.\d+', number).group()) for number in twoyield]

    yinv = []
    for i in range(len(tenyield)):
        yinv.append(tenyield[i] - twoyield[i])

    return yinv, yearlist