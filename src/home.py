import streamlit as st

def show_home_page():
    st.title("Portfolio Manager")

    st.markdown("""
    <h3 style='color:#2E86C1;'>What is Portfolio Management?</h3>
    <p style='color:#F1948A;'>Portfolio management is the process of selecting, managing, and overseeing investments such as stocks, bonds, and other assets, with the goal of achieving specific financial objectives. The essence of portfolio management is to create a balanced and diversified mix of investments that align with an individual's risk tolerance, investment horizon, and financial goals.</p>

    <ul style='color:#9B59B6;'>
        <li><b>Asset Allocation:</b> Choosing the right mix of asset classes like stocks, bonds, real estate, etc., based on your goals.</li>
        <li><b>Risk Management:</b> Identifying and managing the level of risk involved with each investment and the portfolio as a whole.</li>
        <li><b>Performance Monitoring:</b> Regularly tracking the performance of the portfolio and making adjustments as needed.</li>
        <li><b>Rebalancing:</b> Adjusting the portfolio's asset allocation to maintain the desired risk/return profile over time.</li>
    </ul>

    <h3 style='color:#2E86C1;'>Why is Portfolio Management Important?</h3>
    <p style='color:#F1948A;'>Effective portfolio management is critical for anyone looking to maximize returns on their investments while managing risk. Here are some key reasons why it is essential:</p>

    <ul style='color:#9B59B6;'>
        <li><b>Diversification:</b> Spreading investments across multiple asset classes and securities reduces risk and helps protect against market volatility.</li>
        <li><b>Goal-Oriented:</b> It ensures that your investments are aligned with your long-term financial objectives, such as retirement, purchasing a home, or funding education.</li>
        <li><b>Risk Mitigation:</b> By actively managing the balance of risk and return, portfolio management helps mitigate potential losses.</li>
        <li><b>Optimal Returns:</b> It helps in identifying and optimizing investment opportunities that can maximize returns based on your risk tolerance and financial goals.</li>
    </ul>

    <h3 style='color:#2E86C1;'>How Does Portfolio Management Help Users?</h3>
    <p style='color:#F1948A;'>Using a portfolio management app can help users:</p>

    <ul style='color:#9B59B6;'>
        <li><b>Track Investments:</b> Easily monitor various investments in one place, ensuring you have a clear overview of your holdings.</li>
        <li><b>Performance Analytics:</b> Analyze the performance of your portfolio over time, including profit and loss (P&L), dividends, and overall growth.</li>
        <li><b>Rebalancing Alerts:</b> Get notified when it’s time to rebalance your portfolio to maintain your target asset allocation.</li>
        <li><b>Personalized Insights:</b> Receive tailored advice based on your investment behavior and preferences to optimize returns.</li>
        <li><b>Efficient Management:</b> Save time and reduce manual tracking by using automated tools that calculate important metrics like ROI, unrealized gains, and accrued interest.</li>
    </ul>
    """, unsafe_allow_html=True)
