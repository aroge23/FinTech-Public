import requests as req
import re
import datetime
import pandas_datareader as pdd
import time
import lxml.html
import pandas as pd
import datetime
import pandas_datareader.data as web
import csv
from tqdm import trange as timer
import os
import openpyxl as xl
import requests
from openpyxl.styles import PatternFill
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
from RSI import GetRSI
from MACD import computeMACD, ExpMovingAvg
from ShiftDate import shift
import invYield
from yahoo import YahooStats

yearList = []
gspcList = []

# USER INPUT
# start_date = input("What year would you like the data to start from the past 10 years? Please enter in 'yyyy-mm-dd' format: ")

tick = 'ttd'

eps_ttm = float(YahooStats(tick)[1][11])

url = 'https://finance.yahoo.com/quote/' + tick.upper() + '/analysis'
html = requests.get(url)
doc = lxml.html.fromstring(html.content)
tables = doc.xpath('//table[@class="W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)"]')
estimates = tables[5].xpath('.//tr[@class="BdT Bdc($seperatorColor)"]')
growth = float(estimates[4].xpath('.//td[@class="Ta(end) Py(10px)"]')[0].xpath('./text()')[0][:-1]) / 100

ror = 15 / 100

mos = 50 / 100

peratio = growth * 200
url = 'https://www.gurufocus.com/term/pe/' + tick + '/PE-Ratio/'
html = requests.get(url)
doc = lxml.html.fromstring(html.content)
tables = doc.xpath('//table[@class="R10"]')[0]
values = tables.xpath('.//tr')[2].xpath('.//td')
if values[-5].xpath('./text()')[0] != 'PE Ratio':
    newpe = (float(values[-1].xpath('./text()')[0]) + float(values[-5].xpath('./text()')[0])) / 2
    if peratio >  newpe and newpe > 0:
        peratio = newpe
else:
    newpe = (float(values[-1].xpath('./text()')[0]) + float(values[-4].xpath('./text()')[0])) / 2
    if peratio > newpe and newpe > 0:
        peratio = newpe


tenyearearnings = eps_ttm * ((1 + growth) ** 9)
fairvalue = (tenyearearnings * peratio) / ((1 + ror) ** 9)
fairmos = fairvalue * mos
print(fairvalue)









# start_date = "2019-02-14" #<-----------------------------------------------
#
# sYear, sMonth, sDay = int(start_date.split("-")[0]), int(start_date.split("-")[1]), int(start_date.split("-")[2])
# #end_date = input("What year would you like the data to end? Please enter in 'yyyy-mm-dd' format. If you'd like today, then type 'today': ")
#
# end_date = "today" #<------------------------------------------------------
#
# if end_date != "today":
#     eYear, eMonth, eDay = int(end_date.split("-")[0]), int(end_date.split("-")[1]), int(end_date.split("-")[2])
# else:
#     end_date = datetime.datetime.today().strftime("20%y-%m-%d")
#     eYear, eMonth, eDay = int(end_date.split("-")[0]), int(end_date.split("-")[1]), int(end_date.split("-")[2])
#
#
# #PUTS STOCK AND YEAR DATA INTO RESPECTIVE LISTS
# SP500 = web.DataReader(tick.upper(), 'yahoo', datetime.datetime(sYear, sMonth, sDay), end_date)
# SP500 = SP500.rename(columns={"Adj Close" : "AdjClose"})
# cleanData = SP500.AdjClose
# dataFrame = pd.DataFrame(cleanData)
#
# for i in range(len(list(SP500.AdjClose))):
#     yearList.append(dataFrame.index[i].strftime("20%y-%m-%d"))
#     gspcList.append(SP500.loc[yearList[i], "AdjClose"])
#
# # 50 DAY MOVING AVERAGE
# avg50 = web.DataReader(tick.upper(), 'yahoo', shift(tick.upper(), start_date, 50),end_date).rename(
#     columns={"Adj Close": "AdjClose"})
# ma50 = avg50.AdjClose.rolling(window=50).mean()[50:]
# perf_ma50 = ['gain']
# for i in range(1, len(ma50)):
#     if ma50[i] > ma50[i-1]:
#         perf_ma50.append('gain')
#     else:
#         perf_ma50.append('loss')
# ma50 = pd.Series(perf_ma50, index=yearList)
#
#
# # 200 DAY MOVING AVERAGE
# avg200 = web.DataReader(tick.upper(), 'yahoo', shift(tick.upper(), start_date, 200), end_date).rename(
#     columns={"Adj Close": "AdjClose"})
# ma200 = avg200.AdjClose.rolling(window=200).mean()[200:]
# perf_ma200 = ['gain']
# for i in range(1, len(ma200)):
#     if ma200[i] > ma200[i-1]:
#         perf_ma200.append('gain')
#     else:
#         perf_ma200.append('loss')
# ma200 = pd.Series(perf_ma200, index=yearList)
#
# # MACD
# nslow  = 26
# nfast = 12
#
# macd = computeMACD(tick.upper(), start_date, end_date, nslow, nfast)[2]
# perf_macd = ['gain']
# for i in range(1, len(macd)):
#     if macd[i] > macd[i-1]:
#         perf_macd.append('gain')
#     else:
#         perf_macd.append('loss')
# macd = pd.Series(perf_macd, index=yearList)
#
#
# #RSI
# rsi = GetRSI(tick.upper(), start_date, end_date)
# perf_rsi = ['gain']
# for i in range(1, len(rsi)):
#     if rsi[i] > rsi[i-1]:
#         perf_rsi.append('gain')
#     else:
#         perf_rsi.append('loss')
#
# rsi = pd.Series(perf_rsi, index=yearList)
#
#
# #DEPENDENT VARIABLE
# performance = ['gain']
# for i in range(1, len(cleanData)):
#     if cleanData[i] > cleanData[i-1]:
#         performance.append('gain')
#     else:
#         performance.append('loss')
# performance = pd.Series(performance, index=yearList)
#
#
# all_data = {}
# data = [cleanData[12:], ma50[12:], ma200[12:], macd[12:], rsi[12:], performance[12:]]
# types = ['Stock', '50 Day MA', '200 Day MA', 'MACD', 'RSI', 'Performance']
# for i in range(len(data)):
#     all_data[types[i]] = data[i]
#
# df = pd.DataFrame({tic : rev for tic, rev in all_data.items()})
#
# df.to_csv('testdata2.csv', index=False)



#DATA PREPROCESSING

# Importing the dataset
# dataset = pd.read_csv('testdata2.csv')
# X = dataset.iloc[:, 1:-1].values
# y = dataset.iloc[:, -1].values
#
# # # Taking care of missing data
# # from sklearn.impute import SimpleImputer
# # imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
# # imputer.fit(X[:, :])
# # X[:, :] = imputer.transform(X[:, :])
#
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import OneHotEncoder
# ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0, 1, 2, 3])], remainder='passthrough')
# X = np.array(ct.fit_transform(X))
#
# # Encoding the Dependent Variable
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# y = le.fit_transform(y)
#
# # Splitting the dataset into the Training set and Test set
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)
#
# #Training the Multiple Linear Regression model on the Training set
# from sklearn.linear_model import LinearRegression
# regressor = LinearRegression()
# regressor.fit(X_train, y_train)
#
#
# y_pred = regressor.predict(X_test)
# np.set_printoptions(precision=1)
# for i in range(len(y_pred)):
#     if y_pred[i] >= 0.5:
#         y_pred[i] = 1.
#     else:
#         y_pred[i] = 0.
# print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), axis=1))


# today = datetime.datetime.today()
# rsi_pred = GetRSI(tick.upper(), today.strftime("20%y-%m-%d"), today)[0]
# stock_pred = web.DataReader(tick.upper(), 'yahoo', today.strftime("20%y-%m-%d"), datetime.datetime.today()).Close[0]
# macd_pred = computeMACD(tick.upper(), datetime.datetime(today.year, today.month - 3, today.day).strftime("20%y-%m-%d"), today, nslow, nfast)[2][-1]
# ma50_pred = web.DataReader(tick.upper(), 'yahoo', shift(tick.upper(), today.strftime("20%y-%m-%d"), 50), today).Close.rolling(window=50).mean()[-1]
# ma200_pred = web.DataReader(tick.upper(), 'yahoo', shift(tick.upper(), today.strftime("20%y-%m-%d"), 200), today).Close.rolling(window=200).mean()[-1]
# prediction = regressor.predict([[stock_pred, ma50_pred, ma200_pred, macd_pred, rsi_pred]])[0]
# from sklearn.metrics import r2_score
# print(r2_score(y_test, y_pred))
#
#
# if performance[0] == 'gain':
#     if prediction <= 0.5:
#         print('Prediction: gain')
#     else:
#         print('Prediction: loss')
# else:
#     if prediction <= 0.5:
#         print('Prediction: loss')
#     else:
#         print('Prediction: gain')