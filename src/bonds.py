import streamlit as st
from datetime import datetime, timedelta

# Function to calculate accrued interest
def calculate_accrued_interest(issue_date, purchase_date, coupon_rate, face_value, coupon_frequency):
    # Convert strings to datetime
    issue_date = datetime.strptime(issue_date, '%Y-%m-%d')
    purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
    
    # Coupon payment (annual coupon rate multiplied by face value)
    annual_coupon_payment = (coupon_rate / 100) * face_value

    # Determine the number of days in the coupon period based on the coupon frequency
    if coupon_frequency == 'Annual':
        days_in_period = 365
    elif coupon_frequency == 'Semi-Annual':
        days_in_period = 182  # Approximate half-year period
    elif coupon_frequency == 'Quarterly':
        days_in_period = 91   # Approximate quarter-year period
    
    # Find the date of the last coupon payment
    # We assume coupons are paid regularly since the issue date
    days_since_issue = (purchase_date - issue_date).days
    coupon_intervals = days_in_period
    last_coupon_payment = issue_date + ((days_since_issue // coupon_intervals) * timedelta(days=coupon_intervals))
    
    # Calculate days since the last coupon payment
    days_since_last_payment = (purchase_date - last_coupon_payment).days
    
    # Calculate the coupon payment for this period (partial based on time since last payment)
    accrued_interest = (days_since_last_payment / days_in_period) * annual_coupon_payment
    
    return round(accrued_interest, 2)

def show_bonds_page():
    st.title("Bonds Accrued Interest Calculator")
    
    with st.form("bond_form"):
        # Input for bond details
        issue_date = st.date_input("Issue Date (YYYY-MM-DD)", value=datetime.now())
        purchase_date = st.date_input("Purchase Date (YYYY-MM-DD)", value=datetime.now())
        coupon_rate = st.number_input("Coupon Rate (in %)", min_value=0.0, step=0.1)
        face_value = st.number_input("Face Value of the Bond (in currency)", min_value=0.0, step=1.0)
        coupon_frequency = st.selectbox("Coupon Frequency", ["Annual", "Semi-Annual", "Quarterly"])
        
        # Convert dates to strings for calculation
        issue_date_str = issue_date.strftime('%Y-%m-%d')
        purchase_date_str = purchase_date.strftime('%Y-%m-%d')
        
        # Submit button
        submitted = st.form_submit_button("Calculate Accrued Interest")
        
        if submitted:
            # Calculate accrued interest
            accrued_interest = calculate_accrued_interest(issue_date_str, purchase_date_str, coupon_rate, face_value, coupon_frequency)
            st.success(f"The accrued interest is: {accrued_interest} (in currency)")

    st.write("### How is Accrued Interest Calculated?")
    st.write("""
    Accrued interest is the interest that has accumulated on a bond since the last coupon payment. 
    When a bond is sold before its coupon payment date, the buyer pays the seller the accrued interest, in addition to the bond price.
    The formula used is:
    """)

    st.latex(r'''
    \text{Accrued Interest} = \frac{\text{Days Since Last Coupon Payment}}{\text{Days in Coupon Period}} \times \text{Coupon Payment}
    ''')

    st.write("Where **Coupon Payment** is calculated as:")

    st.latex(r'''
    \text{Coupon Payment} = \text{Face Value} \times \text{Coupon Rate}
    ''')
