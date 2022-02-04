import csv
from flask import Flask, render_template, request
from patterns import patterns
import pandas_datareader.data as web
import datetime
import talib

data = {}

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    pattern = request.args.get('pattern', None)
    stocks = {}
    with open('companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company' : row[1]}

    if pattern:
        for tick in data:
            df = data[tick]
            pattern_function = getattr(talib, pattern)


            try:
                result = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = result.tail(5).values
                if any(val > 0 for val in last):
                    stocks[tick][pattern] = 'bullish'
                elif any(val < 0 for val in last):
                    stocks[tick][pattern] = 'bearish'
                else:
                    stocks[tick][pattern] = None

            except:
                print('error')
    empty = (len(data) == 0)
    return render_template('index.html', patterns=patterns, stocks=stocks, current_pattern=pattern, empty=empty)

@app.route('/snapshot')
def snapshot():
    with open('companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            try:
                symbol = company.split(',')[0]
                df = web.DataReader(symbol, 'yahoo', datetime.datetime.today() - datetime.timedelta(5), 'today')
                data[symbol] = df
            except:
                pass
    return {
        'code' : 'success'
    }

Flask.run(app)