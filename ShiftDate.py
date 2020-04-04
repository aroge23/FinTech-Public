import pandas as pd
import pandas_datareader.data as web
import datetime


def shift(stock, start_date, window):
    # CREATES LIST OF STOCK DAYS WITHIN PAST 10 YEARS
    today =datetime.datetime.today()
    sList = web.DataReader(stock, 'yahoo', datetime.datetime(today.year - 10, today.month, today.day), today)
    frame = pd.DataFrame(sList.Close)
    bigyear = []
    for i in range(len(frame)):
        bigyear.append(frame.index[i].strftime("20%y-%m-%d"))

    # SHIFTS DATA LENGTH OF WINDOW FOR SLOW
    date = bigyear[bigyear.index(start_date) - window].split("-")
    sYear, sMonth, sDay = int(date[0]), int(date[1]), int(date[2])

    shiftDate = datetime.datetime(sYear, sMonth, sDay)

    return shiftDate