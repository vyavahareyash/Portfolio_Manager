import streamlit as st
from .db_handler import get_positions,get_transacted_symbols,get_seq_stock_tnx
import plotly.express as px
import pandas as pd

def show_charts(df):
    st.title("Stock Performance and Distribution")

    with st.spinner("Preparing charts..."):
        # Pie Chart for Distribution Based on Quantity
        fig_pie = px.pie(df, names='stock_symbol', values='holding_quantity', title='Stock Quantity Distribution')
        st.plotly_chart(fig_pie)

        # Bar Chart for Performance Based on P&L Percentage
        fig_bar = px.bar(df, x='stock_symbol', y='p&l_%', title='Stock Performance Based on P&L Percentage', labels={'p&l_%': 'P&L (%)'})
        fig_bar.update_traces(marker_color=df['p&l_%'].apply(lambda x: 'green' if x > 0 else 'red'))

        st.plotly_chart(fig_bar)

def show_positions_page():
    
    st.title('Positions')
    
    with st.spinner("Calculating positions..."):
        positions = get_positions()
        st.dataframe(positions)
    
    total_investment = sum(positions['investment_amount'])
    realised_pl = sum(positions['realized_p&l'])
    unrealised_pl = sum(positions['unrealized_p&l'])
    pl_p = (unrealised_pl / total_investment) * 100
    
    
    st.markdown(f"<h4>Total Investment: <span style='color:yellow;'>${total_investment:,.2f}</span></h4>", unsafe_allow_html=True)
    if realised_pl < 0:
        st.markdown(f"<h4>Realised P&L: <span style='color:red;'>${realised_pl:,.2f}</span></h4>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h4>Realised P&L: <span style='color:green;'>${realised_pl:,.2f}</span></h4>", unsafe_allow_html=True)
    if unrealised_pl < 0:
        st.markdown(f"<h4>Unrealised P&L: <span style='color:red;'>${unrealised_pl:,.2f}</span></h4>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h4>Unrealised P&L: <span style='color:green;'>${unrealised_pl:,.2f}</span></h4>", unsafe_allow_html=True)
    if pl_p < 0:
        st.markdown(f"<h4>P&L %: <span style='color:red;'>{pl_p:.2f}%</span></h4>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h4>P&L %: <span style='color:green;'>{pl_p:.2f}%</span></h4>", unsafe_allow_html=True)
    
    
    st.write("Stock transactions")
    
    stock_symbol = st.selectbox("Select stock",get_transacted_symbols())
    
    stock_txn = get_seq_stock_tnx(stock_symbol)
    
    st.dataframe(stock_txn)
    
    show_charts(positions)