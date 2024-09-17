# Imports libs

import base64
import streamlit as st
import time

# Import functions
from src.home import show_home_page
from src.trends import show_trends_page
from src.transactions import show_transactions_page

# StreamLit App Config
st.set_page_config(
    page_title="Portfolio Management",
    page_icon="🪙"
)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpeg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
set_background('assets/bg_1.jpeg')


def menu_bar():
    pages = ['Home', 'Stock Trends', 'Bonds', 'Transactions','Reports']
    menu = st.sidebar.selectbox("Pages",pages)
    if menu == 'Home':
        show_home_page()
    elif menu == 'Stock Trends':
        show_trends_page()
    elif menu == 'Bonds':
        pass
    elif menu == 'Transactions':
        show_transactions_page()
    elif menu == 'Reports':
        pass
    
if __name__ == '__main__':
    menu_bar()