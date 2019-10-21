import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
from ShiftDate import shift

def MovingAvg(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas

def GetRSI(stock, start_date, end_date, window=14):
    # Date
    start = shift(stock, start_date, window)
    end = end_date

    # Get data
    data = web.DataReader(stock, 'yahoo', start, end)
    # Get just the close
    close = data['Adj Close']

    deltas = np.diff(close)
    seed = deltas[:window + 1]
    up = seed[seed >= 0].sum() / window
    down = -seed[seed < 0].sum() / window
    rs = up / down
    rsi = np.zeros_like(close)
    rsi[:window] = 100. - 100. / (1. + rs)

    for i in range(window, len(close)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (window - 1) + upval) / window
        down = (down * (window - 1) + downval) / window

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    rsi = rsi[window:]

    return rsi