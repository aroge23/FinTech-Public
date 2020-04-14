import lxml.html
import openpyxl as xl
import requests
import datetime
import pandas as pd
import os

import xlrd
from openpyxl.workbook import Workbook

def cvt_xls_to_xlsx(src_file_path, dst_file_path):
    book_xls = xlrd.open_workbook(src_file_path)
    book_xlsx = Workbook()

    sheet_names = book_xls.sheet_names()
    for sheet_index, sheet_name in enumerate(sheet_names):
        sheet_xls = book_xls.sheet_by_name(sheet_name)
        if sheet_index == 0:
            sheet_xlsx = book_xlsx.active
            sheet_xlsx.title = sheet_name
        else:
            sheet_xlsx = book_xlsx.create_sheet(title=sheet_name)

        for row in range(0, sheet_xls.nrows):
            for col in range(0, sheet_xls.ncols):
                sheet_xlsx.cell(row = row+1 , column = col+1).value = sheet_xls.cell_value(row, col)

    book_xlsx.save(dst_file_path)

# if os.path.exists('StockScreen.xls') == True:
#     cvt_xls_to_xlsx('StockScreen.xls', 'StockScreen.xlsx')
wb = xl.load_workbook('StockScreen.xlsx')
sheet = wb.active

for i in range(6, 13):
    tick = sheet['B' + str(i)].value
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

    #WRITES 52-WEEK HIGH
    sheet['C' + str(i)] = values[5][values[5].index('-') + 2:]

    #WRITES PREVIOUS CLOSE
    sheet['D' + str(i)] = values[0]

    #WRITES % DD
    sheet['E' + str(i)] = values[13][values[13].index('(') + 1: len(values[13]) - 1]

    #WRITES PUT/CALL
    url = 'https://www.alphaquery.com/stock/' + str(tick.upper()) + '/volatility-option-statistics/30-day/put-call-ratio-volume'
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    below_chart = doc.xpath('//div[@id="below-chart-text"]')[0]
    sheet['H' + str(i)] = below_chart.xpath('.//strong/text()')[0]

    #WRITES CURRENT PE
    sheet['J' + str(i)] = values[10]


sheet['C2'] = datetime.datetime.today().strftime('%e-%b-%y')

wb.save('StockScreen.xlsx')