import sqlite3
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

DATABASE = 'portfolio.db'
TABLE_TRANSACTION ='Transactions'
STOCK_LIST = 'data/sp500_symbols.txt'
TABLE_POSITION = 'Positions'

def get_transacted_symbols():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = f'SELECT DISTINCT stock_symbol FROM {TABLE_TRANSACTION}'
    
    cursor.execute(query)
    
    result = cursor.fetchall()
    
    conn.close()
    
    return [x[0] for x in result]

def add_transaction(transaction_date_str, order_type, stock_symbol, quantity, unit_price):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(f"""INSERT INTO {TABLE_TRANSACTION} (date, order_type, stock_symbol, quantity, unit_price) VALUES (?, ?, ?, ?,?)""", 
                   (transaction_date_str, order_type, stock_symbol, quantity, unit_price))
    
    conn.commit()
    conn.close()
    
def get_all_transactions():
    conn = sqlite3.connect(DATABASE)
    query = f"SELECT * FROM {TABLE_TRANSACTION}"
    
    # Read the data into a DataFrame
    df = pd.read_sql(query, conn)
    
    # Close the connection
    conn.close()
    
    return df
    
def get_holding_stocks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    bought_query = f"SELECT stock_symbol, sum(quantity) FROM {TABLE_TRANSACTION} WHERE order_type = 'Buy' GROUP BY stock_symbol"
    sold_query = f"SELECT stock_symbol, sum(quantity) FROM {TABLE_TRANSACTION} WHERE order_type = 'Sell' GROUP BY stock_symbol"
    
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

# def validate_stock_symbol(stock_symbol):
#     with open(STOCK_LIST, 'r') as file:
#         symbols = [line.strip() for line in file]
        
#     if stock_symbol in symbols:
#         return True
#     else:
#         False
        
        
def get_seq_stock_tnx(stock_symbol):
    conn = sqlite3.connect(DATABASE)
    
    query = f"SELECT date, stock_symbol, unit_price, order_type, quantity FROM transactions WHERE stock_symbol = ?"
    transactions = pd.read_sql(query, conn, params=(stock_symbol,))
    transactions['date'] = pd.to_datetime(transactions['date'])
    transactions = transactions.sort_values(by='date')
    
    conn.close()
    
    return transactions
        
def get_positions():
    conn = sqlite3.connect(DATABASE)
    # cursor = conn.cursor()
    
    df = pd.DataFrame(columns=['stock_symbol', 'total_quantity', 'realized_pl', 'unrealized_pl'])

    
    for stock_symbol in get_transacted_symbols():
        # query = f"SELECT date, stock_symbol, unit_price, order_type, quantity FROM transactions WHERE stock_symbol = ?"
        # transactions = pd.read_sql(query, conn, params=(stock_symbol,))
        # transactions['date'] = pd.to_datetime(transactions['date'])
        # transactions = transactions.sort_values(by='date')
        transactions = get_seq_stock_tnx(stock_symbol)
        total_quantity = 0
        total_cost = 0
        realized_pl = 0 

        for index, row in transactions.iterrows():
            if row['order_type'] == 'Buy':
                # Update total quantity and total cost for buy orders
                total_quantity += row['quantity']
                total_cost += row['unit_price'] * row['quantity']
            
            elif row['order_type'] == 'Sell':
                # Calculate realized profit/loss for sell orders
                avg_buy_price = total_cost / total_quantity if total_quantity > 0 else 0
                # sell_value = row['unit_price'] * row['quantity']
                realized_pl += (row['unit_price'] - avg_buy_price) * row['quantity']
                
                # Update total quantity and total cost
                total_quantity -= row['quantity']
                total_cost = avg_buy_price * total_quantity
                
        # Calculate unrealized profit/loss based on current stock price

        # Get today's date

        # Get date after 10 days
        start_date = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
        end_date = datetime.today().strftime('%Y-%m-%d')
        
        stock_data = get_historical_stock_data(stock_symbol,start_date,end_date)  # Assume a current price, replace with actual
        current_price = stock_data['Close'].iloc[-1]
        avg_buy_price = total_cost / total_quantity if total_quantity > 0 else 0
        unrealized_pl = (current_price - avg_buy_price) * total_quantity
        
        results = [{
            'stock_symbol':stock_symbol,
            'total_quantity':total_quantity,
            'realized_pl':realized_pl,
            'unrealized_pl':unrealized_pl
            }]
        
        df = pd.concat([df, pd.DataFrame(results)], ignore_index=True)

    
    conn.close()
    return df

