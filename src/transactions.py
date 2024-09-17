import streamlit as st
from datetime import datetime
import os
from .db_handler import add_transaction

STOCK_LIST = 'data/sp500_symbols.txt'

def validate_stock_symbol(stock_symbol):
    with open(STOCK_LIST, 'r') as file:
        symbols = [line.strip() for line in file]
        
    if stock_symbol in symbols:
        return True
    else:
        False

def show_transactions_page():
    st.title('Transactions')
    
    st.write('Add new transaction')
    available_stocks = [stock.split('.')[0] for stock in os.listdir('data')]
    with st.form("transaction_form"):
        transaction_date = st.date_input("Transaction Date", value=datetime.now())
        order_type = st.selectbox("Order Type", ["Buy", "Sell"])
        stock_symbol = st.text_input("Stock Symbol (e.g., AAPL)")
        quantity = st.number_input("Quantity", min_value=1)

        # Submit button
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted:
            stock_symbol = stock_symbol.upper()
            if not stock_symbol:
                st.error("Stock symbol is required!")
            elif not validate_stock_symbol(stock_symbol):
                st.error(f"Invalid stock symbol: {stock_symbol}. Please enter a valid symbol.")
            else:
                
                transaction_date_str = transaction_date.strftime("%Y-%m-%d")

                add_transaction(transaction_date_str, order_type, stock_symbol, quantity)

                st.success("Transaction added successfully!")