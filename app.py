from flask import Flask, render_template, request, redirect, url_for, flash
from utils import load_watchlist, save_watchlist, fetch_stock_data

app = Flask(__name__)

app.secret_key = "ABCDEFG"


@app.route('/', methods=['GET', 'POST'])
def index():
    tickers = load_watchlist()
    if request.method == 'POST':
        ticker = request.form.get('ticker').upper().strip()
        if not ticker:
            flash('Please enter a ticker symbol.', 'error')
        else:
            data = fetch_stock_data(ticker)
            if data:
                if ticker not in tickers:
                    tickers.append(ticker)
                    save_watchlist(tickers)
                    flash(f'{ticker} added.', 'success')
                else:
                    flash(f'{ticker} already in list.', 'info')
            else:
                flash(f'Problem with {ticker} symbol.', 'error')
            return redirect(url_for('index'))
    else:
        stocks_data = []
        for ticker in tickers:
            data = fetch_stock_data(ticker)
            if data:
                stocks_data.append(data)

        return render_template('index.html', stocks_data=stocks_data)


@app.route('/remove/<ticker>')
def remove(ticker):
    tickers = load_watchlist()
    if ticker in tickers:
        tickers.remove(ticker)
        save_watchlist(tickers)
        flash(f'{ticker} removed.', 'success')
    else:
        flash(f'{ticker} not in list.', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5011)
