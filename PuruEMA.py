import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd
import datetime

tick = 'IWY'
ser = web.DataReader(tick, 'yahoo', '1-1-20', datetime.datetime.today()).rename(columns={'Adj Close': 'AdjClose'})
df = pd.DataFrame(ser.AdjClose)
df['EMA40'] = ser.AdjClose.ewm(span=40).mean()
df['EMA120'] = ser.AdjClose.ewm(span=120).mean()
df.dropna(inplace=True)

# BASICALLY CREATES A LIST OF ALL THE CROSSOVER DAYS OF THE 40 AND 120 EMA
# THE FIRST VALUE IS THE FIRST DAY AND LAST VALUE IS THE LAST DAY WITH A 5-DAY LEEWAY
crossover = []
for i in range(30, len(df)):
    if df.EMA40.loc[df.index[i]] < df.EMA120.loc[df.index[i]]:
        crossover.append(df.index[i-5])
    if df.EMA40.loc[df.index[i]] > df.EMA120.loc[df.index[i]] and \
        df.EMA40.loc[df.index[i - 1]] < df.EMA120.loc[df.index[i - 1]]:
        crossover.append(df.index[i+5])
        break

plt.figure(figsize=(17, 9))
ax1 = plt.subplot(211)
plt.plot(df.EMA40, c='b', label='EMA40')
plt.plot(df.EMA120, c='m', label='EMA120')
plt.legend(loc=0)
plt.axvline(crossover[0])
plt.axvline(crossover[-1])


df['EMA5'] = ser.AdjClose.ewm(span=5).mean()
df['EMA20'] = ser.AdjClose.ewm(span=20).mean()

ax2 = plt.subplot(212)
plt.plot(df.EMA5, c='b', label='EMA5')
plt.plot(df.EMA20, c='m', label='EMA20')
plt.legend(loc=0)
x1, x2, y1, y2 = crossover[0], crossover[-1], df.min().EMA5 - 10, df.max().EMA5 + 10
plt.xlim(x1, x2)
plt.ylim(y1, y2)

print('Crossover starts: ' + str(crossover[0]))
print('Crossover ends: ' + str(crossover[-1]))

plt.draw()
plt.show()