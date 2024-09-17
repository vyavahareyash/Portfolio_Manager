import streamlit as st 
import os
import pandas as pd
import plotly.express as px


def show_trends_page():
    st.title("Trends Analysis")
    st.write("Welcome to our Trends Analysis Page!")
    
    available_stocks = [stock.split('.')[0] for stock in os.listdir('data')]
    
    selected_stock = st.selectbox('choose a stock',available_stocks)
    
    df = pd.read_csv('data/'+selected_stock+'.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    fig = px.line(df, x='Date', y='Adj Close', title=f'{selected_stock} Stock Price Trend')

    # Display the chart
    st.title('Stock Price Trend')
    st.plotly_chart(fig)