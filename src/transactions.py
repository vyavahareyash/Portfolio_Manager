import streamlit as st
from datetime import datetime
import os
from .db_handler import add_transaction

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
            # Convert date to string
            transaction_date_str = transaction_date.strftime("%Y-%m-%d")
            
            add_transaction(transaction_date_str, order_type, stock_symbol, quantity)
            
            st.success("Transaction added successfully!")