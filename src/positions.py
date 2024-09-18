import streamlit as st
from .db_handler import get_positions,get_transacted_symbols,get_seq_stock_tnx

def show_positions_page():
    
    st.title('Positions')
    
    with st.spinner("Calculating positions..."):
        st.dataframe(get_positions())

    st.write("Stock transactions")
    
    stock_symbol = st.selectbox("Select stock",get_transacted_symbols())
    
    st.dataframe(get_seq_stock_tnx(stock_symbol))