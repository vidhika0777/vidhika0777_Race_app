import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Set date range for historical data
start_date = '2024-01-01'
end_date = '2025-03-31'

# Download stock data for Ferrari and Mercedes-Benz (MBG.DE is listed on XETRA)
ferrari_stock = yf.download('RACE', start=start_date, end=end_date)
mercedes_stock = yf.download('MBG.DE', start=start_date, end=end_date)

# Calculate daily returns and drop NaN values
ferrari_returns = ferrari_stock['Close'].pct_change().dropna()
mercedes_returns = mercedes_stock['Close'].pct_change().dropna()

# Function to calculate Value at Risk (VaR)
def calculate_var(returns, confidence_level):
    return np.percentile(returns, 100 * (1 - confidence_level))

# Compute VaR for both stocks at 95% and 99% confidence levels
var_95_ferrari = calculate_var(ferrari_returns, 0.95)
var_99_ferrari = calculate_var(ferrari_returns, 0.99)
var_95_mercedes = calculate_var(mercedes_returns, 0.95)
var_99_mercedes = calculate_var(mercedes_returns, 0.99)

# Print VaR results
print(f'Ferrari VaR at 95%: {var_95_ferrari:.4f}')
print(f'Ferrari VaR at 99%: {var_99_ferrari:.4f}')
print(f'Mercedes VaR at 95%: {var_95_mercedes:.4f}')
print(f'Mercedes VaR at 99%: {var_99_mercedes:.4f}')

# Plot histograms with VaR lines
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Ferrari
axes[0].hist(ferrari_returns, bins=100, alpha=0.75, label='Ferrari')
axes[0].axvline(x=var_95_ferrari, color='r', linestyle='--', label='VaR 95%')
axes[0].axvline(x=var_99_ferrari, color='g', linestyle='--', label='VaR 99%')
axes[0].set_title('Ferrari Daily Returns')
axes[0].legend()
axes[0].set_xlabel('Daily Return')
axes[0].set_ylabel('Frequency')

# Mercedes
axes[1].hist(mercedes_returns, bins=100, alpha=0.75, label='Mercedes')
axes[1].axvline(x=var_95_mercedes, color='r', linestyle='--', label='VaR 95%')
axes[1].axvline(x=var_99_mercedes, color='g', linestyle='--', label='VaR 99%')
axes[1].set_title('Mercedes Daily Returns')
axes[1].legend()
axes[1].set_xlabel('Daily Return')
axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# Calculate and compare volatility (as float values)
ferrari_volatility = float(ferrari_returns.std())
mercedes_volatility = float(mercedes_returns.std())

print(f'Ferrari Volatility: {ferrari_volatility:.4f}')
print(f'Mercedes Volatility: {mercedes_volatility:.4f}')

# Determine which stock is more volatile
if ferrari_volatility > mercedes_volatility:
    print("Ferrari's stock is more volatile.")
else:
    print("Mercedes' stock is more volatile.")
