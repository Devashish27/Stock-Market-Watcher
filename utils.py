import datetime
import json
import yfinance as yf

WATCHLIST = 'watchlist.json'


def save_watchlist(tickers):
    with open(WATCHLIST, 'w') as f:
        json.dump(tickers, f)


def load_watchlist():
    try:
        with open(WATCHLIST, 'r') as f:
            tickers = json.load(f)
        return tickers
    except FileNotFoundError as e:
        return []


def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            row = data.iloc[-1]
            price = row['Close']
            high = row['High']
            low = row['Low']
            volume = row['Volume']
            prev_close = stock.info.get('previousClose', price)
            change = price - prev_close
            change_pct = (change / prev_close) * 100 if prev_close else 0
            date_time = row.name.strftime('%Y-%m-%d %H:%M:%S')

            return_data = {
                'ticker': ticker,
                'price': f'${price:.2f}',
                'change': change,
                'change_pct': change_pct,
                'date_time': date_time,
                'high': f'${high:.2f}',
                'low': f'${low:.2f}',
                'volume': f'${volume:,}'
            }

            return return_data
        else:
            return None
    except Exception as e:
        return None
