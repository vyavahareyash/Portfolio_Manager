import streamlit as st
from .db_handler import get_positions,get_transacted_symbols,get_seq_stock_tnx

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