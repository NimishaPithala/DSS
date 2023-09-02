from flask import Flask, render_template
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def display_data():
    btc_ticker = yf.Ticker('BTC-USD')
    btc = btc_ticker.history(period='max')
    btc.index = pd.to_datetime(btc.index)
    btc.index = btc.index.tz_localize(None)
    del btc['Dividends']
    del btc['Stock Splits']
    btc.columns = [i.lower() for i in btc.columns]
    btc['tomorrow'] = btc['close'].shift(-1)
    tail = btc.tail()

    # Create a line plot of tomorrow's close price
    plt.figure(figsize=(10, 6))
    plt.plot(tail.index, tail['tomorrow'])
    plt.title("Tomorrow's Close Price of Bitcoin")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)

    # Save the plot as an image file
    plot_filename = 'tomorrow_close_plot.png'
    plt.savefig(plot_filename)

    # Calculate the price difference between today's close and tomorrow's close
    price_today = tail['close'].iloc[-1]
    price_tomorrow = tail['tomorrow'].iloc[-1]
    price_diff = price_tomorrow - price_today

    # Determine whether the price has dropped or not
    if price_diff < 0:
        price_statement = "The price has dropped."
    elif price_diff > 0:
        price_statement = "The price has increased."
    else:
        price_statement = "The price remains unchanged."

    return render_template('index.html', dataframe=tail, plot_filename=plot_filename, price_statement=price_statement)


if __name__ == '__main__':
    app.run()
