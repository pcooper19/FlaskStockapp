"""A simple app that returns the daily moving average of a stock. """"


from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import pandas as pd
import datetime
import pandas_datareader.data as web

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def start():
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():

    if request.method == 'POST':

        start = datetime.datetime(2016, 1, 1)
        end = datetime.datetime.today().strftime('%y-%m-%d')

        #stock = input("Enter the name of the stock\n")
        stock = request.form['ticker'].upper()

        symbol = 'WIKI/'+stock.upper()

        df = web.DataReader(symbol, 'quandl', start, end)

        stockp = df.head(1)['AdjClose'].iloc[0]

        ma = df['AdjClose'].sort_index(ascending=True)

        ma100 = int(ma.rolling(window=100).mean().tail().iloc[4])
        ma50 = int(ma.rolling(window=50).mean().tail().iloc[4])
        ma20 = int(ma.rolling(window=20).mean().tail().iloc[4])
        ma10 = int(ma.rolling(window=10).mean().tail().iloc[4])

    else:
        print("It is not a GET")

    return render_template('result.html',  stockn = stock, stockp = stockp,
        ma100=ma100, ma50=ma50, ma20=ma20, ma10= ma10)





if __name__ == '__main__':
    app.run(debug=True)
