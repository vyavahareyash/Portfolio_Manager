import sqlite3
import yfinance as yf
import pandas as pd

DATABASE = 'portfolio.db'
TABLE ='Transactions'

def add_transaction(transaction_date_str, order_type, stock_symbol, quantity, unit_price):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(f"""INSERT INTO {TABLE} (date, order_type, stock_symbol, quantity, unit_price) VALUES (?, ?, ?, ?,?)""", 
                   (transaction_date_str, order_type, stock_symbol, quantity, unit_price))
    
    conn.commit()
    conn.close()
    
def get_transactions():
    conn = sqlite3.connect(DATABASE)
    query = f"SELECT * FROM {TABLE}"
    
    # Read the data into a DataFrame
    df = pd.read_sql(query, conn)
    
    # Close the connection
    conn.close()
    
    return df
    
    
    
    
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