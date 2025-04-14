import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Streamlit settings
st.set_page_config(page_title="Ferrari vs Mercedes Stock Risk", layout="wide")
st.title("📉 Ferrari (RACE) vs Mercedes-Benz (MBG.DE) Stock Risk Analysis")

# Sidebar: Date range
st.sidebar.header("Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-03-31"))

# Download data function
@st.cache_data
def download_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

# Download stock data
ferrari_stock = download_data('RACE', start_date, end_date)
mercedes_stock = download_data('MBG.DE', start_date, end_date)

# Check if data exists
if ferrari_stock.empty or mercedes_stock.empty:
    st.error("Failed to retrieve stock data. Please check the date range or tickers.")
    st.stop()

# Calculate daily returns
ferrari_returns = ferrari_stock['Close'].pct_change().dropna()
mercedes_returns = mercedes_stock['Close'].pct_change().dropna()

# Function to calculate VaR
def calculate_var(returns, confidence_level):
    return np.percentile(returns, 100 * (1 - confidence_level))

# Calculate VaRs
var_95_ferrari = calculate_var(ferrari_returns, 0.95)
var_99_ferrari = calculate_var(ferrari_returns, 0.99)
var_95_mercedes = calculate_var(mercedes_returns, 0.95)
var_99_mercedes = calculate_var(mercedes_returns, 0.99)

# Calculate volatility
ferrari_volatility = float(ferrari_returns.std())
mercedes_volatility = float(mercedes_returns.std())

# Display metrics
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Ferrari (RACE)")
    st.metric("Volatility", f"{ferrari_volatility:.4f}")
    st.metric("VaR 95%", f"{var_95_ferrari:.4f}")
    st.metric("VaR 99%", f"{var_99_ferrari:.4f}")

with col2:
    st.subheader("🚙 Mercedes-Benz (MBG.DE)")
    st.metric("Volatility", f"{mercedes_volatility:.4f}")
    st.metric("VaR 95%", f"{var_95_mercedes:.4f}")
    st.metric("VaR 99%", f"{var_99_mercedes:.4f}")

# Plotting
st.subheader("📊 Daily Returns Distribution with VaR")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Ferrari Histogram
axes[0].hist(ferrari_returns, bins=100, alpha=0.75, label='Ferrari')
axes[0].axvline(x=var_95_ferrari, color='r', linestyle='--', label='VaR 95%')
axes[0].axvline(x=var_99_ferrari, color='g', linestyle='--', label='VaR 99%')
axes[0].set_title("Ferrari Daily Returns")
axes[0].legend()
axes[0].set_xlabel('Daily Return')
axes[0].set_ylabel('Frequency')

# Mercedes Histogram
axes[1].hist(mercedes_returns, bins=100, alpha=0.75, label='Mercedes')
axes[1].axvline(x=var_95_mercedes, color='r', linestyle='--', label='VaR 95%')
axes[1].axvline(x=var_99_mercedes, color='g', linestyle='--', label='VaR 99%')
axes[1].set_title("Mercedes Daily Returns")
axes[1].legend()
axes[1].set_xlabel('Daily Return')
axes[1].set_ylabel('Frequency')

st.pyplot(fig)

# Volatility Comparison
st.subheader("📈 Volatility Comparison")
if ferrari_volatility > mercedes_volatility:
    st.warning("Ferrari's stock is more volatile.")
else:
    st.info("Mercedes' stock is more volatile.")
