import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
from RSI import GetRSI
from MACD import computeMACD, ExpMovingAvg
from ShiftDate import shift
import invYield

yearList = []
gspcList = []

# USER INPUT
#start_date = input("What year would you like the data to start from the past 10 years? Please enter in 'yyyy-mm-dd' format: ")

start_date = "2017-02-14" #<-----------------------------------------------

sYear, sMonth, sDay = int(start_date.split("-")[0]), int(start_date.split("-")[1]), int(start_date.split("-")[2])
#end_date = input("What year would you like the data to end? Please enter in 'yyyy-mm-dd' format. If you'd like today, then type 'today': ")

end_date = "today" #<------------------------------------------------------

if end_date != "today":
    eYear, eMonth, eDay = int(end_date.split("-")[0]), int(end_date.split("-")[1]), int(end_date.split("-")[2])
else:
    end_date = datetime.datetime.today().strftime("20%y-%m-%d")
    eYear, eMonth, eDay = int(end_date.split("-")[0]), int(end_date.split("-")[1]), int(end_date.split("-")[2])


#PUTS STOCK AND YEAR DATA INTO RESPECTIVE LISTS
SP500 = web.DataReader('^GSPC', 'yahoo', datetime.datetime(sYear, sMonth, sDay), end_date)
SP500 = SP500.rename(columns={"Adj Close" : "AdjClose"})
cleanData = SP500.AdjClose
dataFrame = pd.DataFrame(cleanData)

for i in range(len(list(SP500.AdjClose))):
    yearList.append(dataFrame.index[i].strftime("20%y-%m-%d"))
    gspcList.append(SP500.loc[yearList[i], "AdjClose"])

# 50 DAY MOVING AVERAGE
avg50 = web.DataReader('^GSPC', 'yahoo', shift('^GSPC', start_date, 50),end_date).rename(
    columns={"Adj Close": "AdjClose"})
ma50 = avg50.AdjClose.rolling(window=50).mean()
df50 = pd.DataFrame(ma50)

short_moving_avg = []
for i in range(50, len(df50)):
    short_moving_avg.append(ma50.loc[df50.index[i].strftime("20%y-%m-%d")])


# 200 DAY MOVING AVERAGE
avg200 = web.DataReader('^GSPC', 'yahoo', shift('^GSPC', start_date, 200), end_date).rename(
    columns={"Adj Close": "AdjClose"})
ma200 = avg200.AdjClose.rolling(window=200).mean()
df200 = pd.DataFrame(ma200)

long_moving_avg = []
for i in range(200, len(df200)):
    long_moving_avg.append(ma200.loc[df200.index[i].strftime("20%y-%m-%d")])

all_data = {}
data = [cleanData, ma50[50:], ma200[200:]]
types = ['Stock', '50 Day MA', '200 Day MA']
for i in range(3):
    all_data[types[i]] = data[i]
df = pd.DataFrame({tic : rev for tic, rev in all_data.items()})

writer = pd.ExcelWriter('testgraph.xlsx', engine='xlsxwriter', datetime_format='YYYY-MM-DD')
df.to_excel(writer, sheet_name= 'Sheet1')

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
workbook = writer.book
worksheet = writer.sheets['Sheet1']

# Adjust the width of the first column to make the date values clearer.
worksheet.set_column('A:A', 20)
worksheet.set_column('C:C', 10)
worksheet.set_column('D:D', 10)

# Create a chart object
chart = workbook.add_chart({'type' : 'line'})
chart.set_size({'x_scale' : 1.5, 'y_scale' : 1.5})

# Configure the series of the chart from the dataframe data
max_row = len(df) + 1
for i in range(len(types)):
    col = i + 1
    chart.add_series({
        'name': ['Sheet1', 0, col],
        'categories': ['Sheet1', 2, 0, max_row, 0],
        'values': ['Sheet1', 2, col, max_row, col],
        'line': {'width': 1.5}
    })

# Configure the chart axes.
chart.set_x_axis({
    'name': 'Date',
    'date_axis': True,
    'name_font' : {'size' : 16}
})
chart.set_y_axis({
    'name': 'Price',
    'major_gridlines': {'visible': False}
})

# Position the legend at the top of the chart.
chart.set_legend({'position': 'top'})

# Insert the chart into the worksheet.
worksheet.insert_chart('H2', chart)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

print(df)


# #CIRCLE FUNCTION
# def circle(x, y, graph, radius):
#     from matplotlib.patches import Circle
#     from matplotlib.patheffects import withStroke
#     circle = Circle((x, y), radius, clip_on=False, zorder=10, linewidth=1,
#                     edgecolor='white', facecolor=(0, 1, 0, .0125),
#                     path_effects=[withStroke(linewidth=1, foreground='w')])
#     graph.add_artist(circle)
#
#
# plt.figure(figsize=(20, 9.75), facecolor="#07000d")
# #PLOT STOCK, MOVING AVG 50, AND MOVING AVG 200
# ax2 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=5, facecolor="#07000d")
# ax2.plot(yearList, short_moving_avg, zorder=10, color="#f421ff")
# ax2.plot(yearList, long_moving_avg, zorder=10, color="#2205fa")
# ax2.plot(yearList, gspcList, zorder=-10, color="#05fa22")
# plt.setp(ax2.get_xticklabels(), visible=False)
#
# #PLOT CIRCLE ON INDICATOR
# for i in range(len(yearList)-1):
#     if short_moving_avg[i] < long_moving_avg[i]:
#         circle(yearList[i-1], short_moving_avg[i]+5, ax2, 7)
#         break
#
# #CONFIGURE THE LEGEND
# maLeg = ax2.legend(["50 Day Avg", "200 Day Avg", "GSPC Stock"], loc=9, shadow=True, fancybox=True, ncol=2, borderaxespad=0.)
# maLeg.get_frame().set_alpha(0.4)
# textEd = plt.gca().get_legend().get_texts()
# plt.setp(textEd[0:5], color="w")
#
# #SETS COLOR, LABELS, AND TICKS
# ax2.set_ylabel("Stock Value")
# ax2.tick_params(axis="x", colors="w")
# ax2.tick_params(axis="y", colors="w")
# ax2.xaxis.label.set_color("w")
# ax2.xaxis.set_major_locator(plt.MaxNLocator(30))
# ax2.spines['bottom'].set_color("#dddddd")
# ax2.spines['top'].set_color("#dddddd")
# ax2.spines['right'].set_color("#dddddd")
# ax2.spines['left'].set_color("#dddddd")
#
#
# #MACD
# axm = plt.subplot2grid((6, 4), (5, 0), sharex=ax2, rowspan=1, colspan=4, facecolor="#07000d")
# nslow = 26
# nfast = 12
# nema = 9
#
# emaslow, emafast, macd = computeMACD("^GSPC", start_date, end_date, nslow, nfast)
# ema9 = ExpMovingAvg(macd, nema)
#
# axm.plot(yearList, macd, color="#5ca3e6")
# axm.plot(yearList, ema9, color="#ada311")
# fill = (macd - ema9)
# axm.fill_between(yearList, fill, 0, alpha=0.5, facecolor="#db44a1", edgecolor="#e874c7")
# #plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune="upper"))
# axm.xaxis.set_major_locator(plt.MaxNLocator(30))
#
#
# #LABELS
# axm.spines['bottom'].set_color("#dddddd")
# axm.spines['top'].set_color("#dddddd")
# axm.spines['right'].set_color("#dddddd")
# axm.spines['left'].set_color("#dddddd")
# axm.tick_params(axis="x", colors="w")
# axm.tick_params(axis="y", colors="w")
# axm.set_xlabel("Year")
# axm.yaxis.label.set_color("w")
# plt.ylabel("MACD", color="w")
# for tick in axm.get_xticklabels():
#     tick.set_rotation(80)
#
# cdLeg = axm.legend(["MACD", "Signal Line"], loc="lower left", shadow=True, fancybox=True, ncol=2, borderaxespad=0.)
# cdLeg.get_frame().set_alpha(0.4)
# textEd2 = plt.gca().get_legend().get_texts()
# plt.setp(textEd2[0:5], color="w")
#
#
# #ALL UPTICKS AND DOWNTICKS IN GRAPH
# upsum = 0
# for i in range(len(gspcList)-1):
#     if gspcList[i+1] > gspcList[i]:
#         upsum += (gspcList[i+1] - gspcList[i])
#
# downsum = 0
# for i in range(len(gspcList)-1):
#     if gspcList[i+1] < gspcList[i]:
#         downsum += (gspcList[i] - gspcList[i+1])
#
#
# #SCORE SYSTEM FOR RSI AND MACD
# uparrRSI = []
# weightsRSI = []
# rsi = GetRSI("^GSPC", start_date, end_date)
#
# uparrMACD = []
# weightsMACD = []
# macd = computeMACD("^GSPC", start_date, end_date, nslow, nfast)[2]
#
# for i in range(len(gspcList) - 5):
#     if gspcList[i+5] - gspcList[i] >= 70:
#         uparrRSI.append(rsi[i+3])
#         uparrMACD.append(macd[i+3])
#         weightsRSI.append((gspcList[i+5] - gspcList[i]) / upsum)
#         weightsMACD.append((gspcList[i+5] - gspcList[i]) / upsum)
# optimalRSIarr = []
# optimalMACDarr = []
# for i in range(len(uparrRSI)):
#     optimalRSIarr.append(uparrRSI[i] * weightsRSI[i])
#     optimalMACDarr.append(uparrMACD[i] * weightsMACD[i])
# optimalRSI = np.sum(optimalRSIarr)
# optimalMACD = np.sum(optimalMACDarr)
#
# #scoreRSI = []
# #scoreMACD = []
# #for i in range(len(rsi)):
# #    scoreRSI.append(optimalRSI / rsi[i])
# #    scoreMACD.append(optimalMACD / macd[i])
#
# #DETERMINE UNOPTIMAL RSI VALUE
# downRSI = []
# weightsRSI = []
#
# for i in range(len(gspcList) - 5):
#     if gspcList[i] - gspcList[i+5] >= 40:
#         downRSI.append(rsi[i+3])
#         weightsRSI.append((gspcList[i] - gspcList[i+5]) / downsum)
# unoptimalRSIarr = []
# for i in range(len(downRSI)):
#     unoptimalRSIarr.append(downRSI[i] * weightsRSI[i])
# unoptimalRSI = np.sum(unoptimalRSIarr) - 1
#
# #PLOT RSI LINE
# ax1 = plt.subplot2grid((6,4), (0,0), rowspan=1, colspan=4, facecolor="#07000d", sharex=ax2)
# ax1.plot(yearList, rsi)
# ax1.xaxis.set_major_locator(plt.MaxNLocator(30))
# ax1.set_ylim(10, 90)
#
# #TITLE, TICKS, COLORS, AND LABELS
# ax1.set_title("S&P500", color="w")
# ax1.tick_params(axis="x", colors="w")
# ax1.tick_params(axis="y", colors="w")
# ax1.spines['bottom'].set_color("#dddddd")
# ax1.spines['top'].set_color("#dddddd")
# ax1.spines['right'].set_color("#dddddd")
# ax1.spines['left'].set_color("#dddddd")
# plt.ylabel("RSI")
# ax1.yaxis.label.set_color("w")
# plt.setp(ax1.get_xticklabels(), visible=False)
#
# #HORIZONTAL LINES
# #unoptimalRSI, optimalRSI = 70, 30
# ax1.axhline(int(unoptimalRSI), color="r", linewidth=0.5)
# ax1.axhline(int(optimalRSI), color="g", linewidth=0.5)
# ax1.set_yticks([int(optimalRSI), int(unoptimalRSI)])
#
# #ASSIGN STANDARD DEVIATIONS FROM OPTIMAL RSI
# rsiSTD = np.std(rsi)
# scoreRSI = []
# for i in range(len(rsi)):
#     scoreRSI.append((rsi[i] - unoptimalRSI) / rsiSTD)
#
# macdSTD = np.std((fill))
# scoreMACD = []
# for i in range(len(fill)):
#     scoreMACD.append((fill[i] - 0) / macdSTD)
#
#
# #PLOT CIRCLE ON INDICATOR
# temp = False
# for i in range(len(yearList)-1):
#     if scoreRSI[i] > 0:
#         if temp == False:
#             circle(yearList[i-1], rsi[i], ax1, 4)
#             temp = True
#     if temp == True:
#         if scoreRSI[i] < 0:
#             temp = False
#
# macdlist = []
# for i in range(len(macd)):
#     macdlist.append(int((macd[i] - ema9[i]) * 100))
#     if macdlist[i] > 999 or macdlist[i] < -999:
#         macdlist[i] = int(macdlist[i] / 10)
# for i in range(len(yearList)-1):
#     if macdlist[i] >= -100 and macdlist[i] <= 100:
#         circle(yearList[i-1], (fill)[i], axm, 2)
#
# ax2.annotate("Predicting Potential Pullback: " + str(temp), xy=(0.98, 0.01), xycoords="axes fraction", color="w", horizontalalignment="right")
#
#
#
# #YIELD CURVE IMPLEMENTATION
# yinv, yieldyear = invYield.yieldInv(start_date, end_date)
#
#
# #SETUP THE GRAPH AND PLOT
# plt.figure(figsize=(10, 4.875), facecolor="#07000d")
# y1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=5, facecolor="#07000d")
# y1.plot(yieldyear, yinv, zorder=10, color="#5ffdab") #green
# y1.tick_params(axis="x", colors="w")
# y1.tick_params(axis="y", colors="w")
# for tick in y1.get_xticklabels():
#     tick.set_rotation(80)
# cdLeg = y1.legend(["10 Year - 2 Year Treasury Yield"], loc="lower left", shadow=True, fancybox=True, ncol=2, borderaxespad=0.)
# cdLeg.get_frame().set_alpha(0.4)
# textEd2 = plt.gca().get_legend().get_texts()
# plt.setp(textEd2[0:5], color="w")
# y1.spines['bottom'].set_color("#dddddd")
# y1.spines['top'].set_color("#dddddd")
# y1.spines['right'].set_color("#dddddd")
# y1.spines['left'].set_color("#dddddd")
# y1.xaxis.set_major_locator(plt.MaxNLocator(30))
# y1.set_title("Yield Curve", color="w")
# y1.axhline(1, color="y", linewidth=0.5)
# y1.axhline(0, color="r", linewidth=0.5)



#SHOW THE GRAPH
plt.show()



#FOR DISPLAY, USE 2018-02-14 FOR START AND TODAY END
#FOR DEMONSTRATE, USE 2017-02-14 FOR START AND 2018-09-20 FOR END AND INCREASE END BY 1 MONTH FOR RECESSION