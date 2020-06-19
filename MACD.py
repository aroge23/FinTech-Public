import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
from ShiftDate import shift

def ExpMovingAvg(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode="full")[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(stock, start_date, end_date, slow, fast):
    # Date
    startSlow = shift(stock, start_date, slow)
    endSlow = end_date

    # Get data
    dataSlow = web.DataReader(stock, 'yahoo', startSlow, endSlow)
    # Get just the close
    closeSlow = dataSlow['Adj Close']
    closeSlow = closeSlow[slow:]

    #ALL FOR FAST
    # Date
    startFast = shift(stock, start_date, fast)
    endFast = end_date

    # Get data
    dataFast = web.DataReader(stock, 'yahoo', startFast, endFast)
    # Get just the close
    closeFast = dataFast['Adj Close']
    closeFast = closeFast[fast:]

    emaslow = ExpMovingAvg(closeSlow, slow)
    emafast = ExpMovingAvg(closeFast, fast)

    return emaslow, emafast, emafast - emaslow