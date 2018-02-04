"""A simple app that returns the daily moving average of a stock. """


from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import pandas as pd
import datetime
import pandas_datareader.data as web
import traceback

app = Flask(__name__)
Bootstrap(app)


#Create a global dictionary to store the tickers
app.vars= {}

@app.route('/')
def start():
    return redirect('/index')

@app.route('/index')
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect('/result')

@app.route('/result', methods=['GET','POST'])
def result():
        #We are going to try and get the stock data
        # Request is a POST

        app.vars['ticker'] = request.form['ticker'].upper()

        start = datetime.datetime(2016, 1, 1)
        #end = datetime.datetime(2018, 1, 1)
        end = datetime.datetime.now()
        #end = datetime.datetime.today().strftime('%y-%m-%d')

        symbol = 'WIKI/'+ app.vars['ticker']

        if not symbol == '':
            df = web.DataReader(symbol, 'quandl', start, end)

        stockp = df.head(1)['AdjClose'].iloc[0]

        ma = df['AdjClose'].sort_index(ascending=True)

        ma100 = int(ma.rolling(window=100).mean().tail().iloc[4])
        ma50 = int(ma.rolling(window=50).mean().tail().iloc[4])
        ma20 = int(ma.rolling(window=20).mean().tail().iloc[4])
        ma10 = int(ma.rolling(window=10).mean().tail().iloc[4])

        return render_template('result.html',  stockn = app.vars['ticker'], stockp = stockp,
        ma100=ma100, ma50=ma50, ma20=ma20, ma10= ma10)


# @app.errorhandler(500)
# def error_handler(e):
#     return render_template("error.html")

# @app.errorhandler(404)
# def error_handler(e):
#     return render_template("error.html")





if __name__ == '__main__':
    app.run()
