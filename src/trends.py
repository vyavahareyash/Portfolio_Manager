import streamlit as st 
import os
import pandas as pd
import plotly.express as px
# from .transactions import validate_stock_symbol
from datetime import datetime
from .db_handler import get_historical_stock_data, get_all_stock_symbols

def show_trends_page():
    st.title("Trend Analysis")
    st.write("Welcome to our Trends Analysis Page!")
    with st.form("transaction_form"):
        stock_symbol =  st.selectbox("Stock Symbol", get_all_stock_symbols())
        start_date = st.date_input("Start Date", value=datetime.now())
        end_date = st.date_input("End Date", value=datetime.now())
        
        submitted = st.form_submit_button("Show Trend")
        
        if submitted:
        
            stock_symbol = stock_symbol.upper()
            if not stock_symbol:
                st.error("Stock symbol is required!")
            # elif not validate_stock_symbol(stock_symbol):
            #     st.error(f"Invalid stock symbol: {stock_symbol}. Please enter a valid symbol.")
            else:
                with st.spinner("Fetching data..."):
                    stock_data = get_historical_stock_data(stock_symbol, start_date, end_date)
                if stock_data is None:
                    st.error("Could not get stock data.")
                else:
                    st.title('Stock Price Trend')
                    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                    
                    with st.spinner('Loading chart...'):
                        fig = px.line(stock_data, x='Date', y='Close', title=f'{stock_symbol} Stock Price Trend')
                        # Display the chart
                        st.plotly_chart(fig)