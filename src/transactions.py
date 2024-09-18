import streamlit as st
from datetime import datetime, timedelta
import os
from .db_handler import add_transaction, get_historical_stock_data, get_transactions

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
    with st.form("transaction_form"):
        transaction_date = st.date_input("Transaction Date", value=datetime.now())
        order_type = st.selectbox("Order Type", ["Buy", "Sell"])
        stock_symbol = st.text_input("Stock Symbol (e.g., AAPL)")
        quantity = st.number_input("Quantity", min_value=1)
        get_price_clicked = st.form_submit_button("Get Price")
        
        transaction_date_str = transaction_date.strftime("%Y-%m-%d")
        start_date = transaction_date_str
        transaction_date = datetime.strptime(start_date, "%Y-%m-%d")
        new_date = transaction_date + timedelta(days=10)
        end_date = new_date.strftime("%Y-%m-%d")
        
        if get_price_clicked:
            stock_symbol = stock_symbol.upper()
            if not stock_symbol:
                st.error("Stock symbol is required!")
            elif not validate_stock_symbol(stock_symbol):
                st.error(f"Invalid stock symbol: {stock_symbol}. Please enter a valid symbol.")
            else:
                # transaction_date_str = transaction_date.strftime("%Y-%m-%d")
                # start_date = transaction_date_str
                # transaction_date = datetime.strptime(start_date, "%Y-%m-%d")
                # new_date = transaction_date + timedelta(days=10)
                # end_date = new_date.strftime("%Y-%m-%d")
                
                with st.spinner("Getting price..."):
                    stock_data = get_historical_stock_data(stock_symbol, start_date, end_date)
                
                if stock_data is None:
                    st.error(f"Could not fetch price for {stock_symbol} on {transaction_date_str}.")
                else:
                    unit_price = stock_data['Close'][0]
                    st.markdown(f"<h4>Unit price: <span style='color:yellow;'>${unit_price:.2f}</span></h4>", unsafe_allow_html=True)
                    total_price = unit_price * quantity
                    st.markdown(f"<h4>Total price: <span style='color:yellow;'>${total_price:.2f}</span></h4>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Add Transaction")
        if submitted:            
            with st.spinner("Getting price..."):
                stock_data = get_historical_stock_data(stock_symbol, start_date, end_date)
            
            # unit_price = stock_data['Close'][0]
            if stock_data is None:
                st.error("Could not fetch price for {stock_symbol} on {transaction_date_str}.")
            else:
                unit_price = stock_data['Close'][0]
                with st.spinner("Adding transaction..."):
                    add_transaction(transaction_date_str, order_type, stock_symbol, quantity, unit_price)
                    st.success("Transaction added successfully!")
    
    with st.spinner("Loading transactions..."):
        all_transactions = get_transactions()
    st.title("All Transactions")
    st.dataframe(all_transactions)