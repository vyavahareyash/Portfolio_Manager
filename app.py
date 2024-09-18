# Imports libs

import base64
import streamlit as st
import time

# Import functions
from src.home import show_home_page
from src.trends import show_trends_page
from src.transactions import show_transactions_page
from src.positions import show_positions_page
# from src.db_handler import init_db



# StreamLit App Config
st.set_page_config(
    page_title="Portfolio Management",
    page_icon="🪙"
)

# Inject custom CSS to change the form background
st.markdown(
    """
    <style>
    /* Change the form background color */
    .form-container {
        background-color: rgba(0, 0, 0, 0.8);
        padding: 20px;
        border-radius: 10px;
        max-width: 600px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# # Inject custom CSS to change the text color
# st.markdown(
#     """
#     <style>
#     .stApp {
#         color: black;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

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
    
set_background('assets/bg_2.jpg')


def menu_bar():
    pages = ['Home', 'Stock Trends', 'Bonds', 'Transactions','Positions']
    menu = st.sidebar.selectbox("Pages",pages)
    if menu == 'Home':
        show_home_page()
    elif menu == 'Stock Trends':
        show_trends_page()
    elif menu == 'Bonds':
        pass
    elif menu == 'Transactions':
        show_transactions_page()
    elif menu == 'Positions':
        show_positions_page()
    
if __name__ == '__main__':
    menu_bar()