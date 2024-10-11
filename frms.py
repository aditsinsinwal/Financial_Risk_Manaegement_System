import yfinance as yf
import pymysql


db = pymysql.connect(host='localhost', user='user', password='password', db='financial_db')

def load_asset_data(ticker):
    asset = yf.Ticker(ticker)
    data = asset.history(period="5y")
    
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO assets (asset_name, asset_type, current_value) VALUES ('{ticker}', 'stock', {data['Close'][-1]})")
    
    for date, row in data.iterrows():
        cursor.execute(f"INSERT INTO transactions (asset_id, transaction_date, transaction_type, quantity, price) VALUES (1, '{date}', 'buy', 100, {row['Close']})")
    
    db.commit()

load_asset_data('AAPL')



import numpy as np

def calculate_var(returns, confidence_level=0.95):
    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    var = sorted_returns[index]
    return var
def get_asset_returns(asset_id):
    cursor = db.cursor()
    query = f"SELECT price FROM transactions WHERE asset_id = {asset_id}"
    cursor.execute(query)
    prices = cursor.fetchall()
    
    returns = np.diff([p[0] for p in prices]) / [p[0] for p in prices][:-1]
    return returns

returns = get_asset_returns(1)  # Asset ID 1 (e.g., AAPL)
var_95 = calculate_var(returns, confidence_level=0.95)
print(f"95% VaR: {var_95}")

def stress_test(portfolio_id, shock_percentage=-0.2):
    cursor = db.cursor()
    query = f"SELECT a.asset_id, a.current_value, pa.quantity FROM assets a JOIN portfolio_assets pa ON a.asset_id = pa.asset_id WHERE pa.portfolio_id = {portfolio_id}"
    cursor.execute(query)
    portfolio = cursor.fetchall()

    total_loss = 0
    for asset_id, current_value, quantity in portfolio:
        shocked_value = current_value * (1 + shock_percentage)
        loss = (current_value - shocked_value) * quantity
        total_loss += loss

    print(f"Total loss under {shock_percentage*100}% market drop: {total_loss}")
stress_test(1, shock_percentage=-0.2)

import matplotlib.pyplot as plt
import pandas as pd

def plot_asset_prices(asset_id):
    cursor = db.cursor()
    query = f"SELECT transaction_date, price FROM transactions WHERE asset_id = {asset_id}"
    cursor.execute(query)
    data = cursor.fetchall()
    
    df = pd.DataFrame(data, columns=['date', 'price'])
    df['date'] = pd.to_datetime(df['date'])
    
    plt.plot(df['date'], df['price'])
    plt.title(f"Asset ID {asset_id} Price History")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

plot_asset_prices(1)
