import streamlit as st
from datetime import datetime, timedelta
import os
from .db_handler import add_transaction, get_historical_stock_data, get_all_transactions, get_holding_stocks, get_all_stock_symbols#, validate_stock_symbol
import random

def random_date_from_last_10_years():
    today = datetime.today()
    ten_years_ago = today - timedelta(days=365*10)
    random_days = random.randint(0, (today - ten_years_ago).days)
    random_date = ten_years_ago + timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d')


def show_transactions_page():
    st.title('Transactions')
    
    st.write('Add manual transaction')
    
    order_type = st.selectbox("Order Type", ["Buy", "Sell"])
    
    available_stocks = get_holding_stocks()
    
    with st.form("maual_transaction_form"):
        transaction_date = st.date_input("Transaction Date", value=datetime.now())
        
        if order_type == 'Sell':

            if available_stocks:
                stock_symbol = st.selectbox("Stock Symbol", list(available_stocks.keys()))
            else:
                st.warning("No available stocks to sell.")
                stock_symbol = None
        
        else:
            stock_symbol = st.selectbox("Stock Symbol", get_all_stock_symbols())
        
        quantity = st.number_input("Quantity", min_value=1)
        
        get_price_clicked = st.form_submit_button("Get Price")
        
        transaction_date_str = transaction_date.strftime("%Y-%m-%d")
        start_date = transaction_date_str
        transaction_date = datetime.strptime(start_date, "%Y-%m-%d")
        new_date = transaction_date + timedelta(days=10)
        end_date = new_date.strftime("%Y-%m-%d")
        
        if stock_symbol:
            stock_symbol = stock_symbol.upper()
            
        if get_price_clicked:
            if not stock_symbol:
                st.error("Stock symbol is required!")
            # elif not validate_stock_symbol(stock_symbol):
            #     st.error(f"Invalid stock symbol: {stock_symbol}. Please enter a valid symbol.")
            else:                
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
            flag = False
            if order_type == 'Sell':
                quantity_available = available_stocks.get(stock_symbol)
                if not quantity_available:
                    st.error(f"Stock {stock_symbol} not available in your portfolio.")
                    flag=True
                elif quantity > quantity_available:
                    st.error(f"Insufficient quantity for {stock_symbol}. You have {available_stocks[stock_symbol]} shares.")
                    flag=True

            if not flag:
                with st.spinner("Getting price..."):
                    stock_data = get_historical_stock_data(stock_symbol, start_date, end_date)
                if stock_data is None:
                    st.error("Could not fetch price for {stock_symbol} on {transaction_date_str}.")
                else:
                    unit_price = stock_data['Close'][0]
                    with st.spinner("Adding transaction..."):
                        add_transaction(transaction_date_str, order_type, stock_symbol, quantity, unit_price)
                        st.success("Transaction added successfully!")
    
    st.write('Add Random Transactions')
    with st.form("random_transaction_form"):
        no_txn = st.number_input("No. of transactions", min_value=1)
        submitted = st.form_submit_button("Add Random Transaction")
        if submitted:
            with st.spinner("Adding transactions..."):
                all_stocks = get_all_stock_symbols()
                while no_txn>0:
                    available_stocks = get_holding_stocks()
                    order_type = random.choice(['Buy','Sell'])
                    
                    transaction_date_str = random_date_from_last_10_years()
                    start_date = transaction_date_str
                    transaction_date = datetime.strptime(start_date, "%Y-%m-%d")
                    new_date = transaction_date + timedelta(days=10)
                    end_date = new_date.strftime("%Y-%m-%d")
                    transaction_date_str = transaction_date.strftime("%Y-%m-%d")
                    
                    
                    if order_type == 'Buy':
                        stock_symbol = random.choice(all_stocks)
                        quantity = random.randint(1, 100)
                    else:
                        if not len(available_stocks) > 0:
                            continue
                        stock_symbol = random.choice(list(available_stocks.keys()))
                        quantity_available = available_stocks.get(stock_symbol)
                        if not quantity_available>0:
                            continue
                        quantity = random.randint(1, quantity_available)
                        
                    stock_data = get_historical_stock_data(stock_symbol, start_date, end_date)
                        
                    if stock_data is None:
                        continue
                    else:
                        unit_price = stock_data['Close'][0]
                        add_transaction(transaction_date_str, order_type, stock_symbol, quantity, unit_price)
                        no_txn-=1
            st.success("Transaction added successfully!")
                
    with st.spinner("Loading transactions..."):
        all_transactions = get_all_transactions()
    st.title("All Transactions")
    st.dataframe(all_transactions)