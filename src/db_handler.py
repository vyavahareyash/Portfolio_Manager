import sqlite3
import yfinance as yf
import pandas as pd

DATABASE = 'portfolio.db'
TABLE ='Transactions'
STOCK_LIST = 'data/sp500_symbols.txt'

def add_transaction(transaction_date_str, order_type, stock_symbol, quantity, unit_price):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(f"""INSERT INTO {TABLE} (date, order_type, stock_symbol, quantity, unit_price) VALUES (?, ?, ?, ?,?)""", 
                   (transaction_date_str, order_type, stock_symbol, quantity, unit_price))
    
    conn.commit()
    conn.close()
    
def get_all_transactions():
    conn = sqlite3.connect(DATABASE)
    query = f"SELECT * FROM {TABLE}"
    
    # Read the data into a DataFrame
    df = pd.read_sql(query, conn)
    
    # Close the connection
    conn.close()
    
    return df
    
def get_holding_stocks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    bought_query = f"SELECT stock_symbol, sum(quantity) FROM {TABLE} WHERE order_type = 'Buy' GROUP BY stock_symbol"
    sold_query = f"SELECT stock_symbol, sum(quantity) FROM {TABLE} WHERE order_type = 'Sell' GROUP BY stock_symbol"
    
    cursor.execute(bought_query)
    stocks_bought = cursor.fetchall()
    stocks_bought = dict(stocks_bought)
    
    cursor.execute(sold_query)
    stocks_sold = cursor.fetchall()
    stocks_sold = dict(stocks_sold)
     
    available_stocks = {}
    
    for stock, buy_qty in stocks_bought.items():
        sell_qty = stocks_sold.get(stock, 0)  # Get the sell quantity, default to 0 if not sold
        available_qty = buy_qty - sell_qty
        
        if available_qty > 0:
            available_stocks[stock] = available_qty
    
    conn.close()
    
    return available_stocks
    
    
def get_historical_stock_data(symbol, start_date, end_date):
    """
    Fetch historical data for a given stock symbol using yfinance.
    
    Parameters:
    - symbol (str): The stock ticker (e.g., 'AAPL').
    - start_date (str): The start date for fetching data (YYYY-MM-DD).
    - end_date (str): The end date for fetching data (YYYY-MM-DD).
    
    Returns:
    - DataFrame: A pandas DataFrame with the historical data.
    """
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    if stock_data.empty:
        return None
    
    return stock_data.reset_index()

def get_all_stock_symbols():
    with open(STOCK_LIST, 'r') as file:
        symbols = [line.strip() for line in file]
    return symbols

def validate_stock_symbol(stock_symbol):
    with open(STOCK_LIST, 'r') as file:
        symbols = [line.strip() for line in file]
        
    if stock_symbol in symbols:
        return True
    else:
        False