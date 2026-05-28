import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

nifty50 = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS",
    "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "BPCL.NS", "BHARTIARTL.NS", "BRITANNIA.NS", "CIPLA.NS",
    "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", "EICHERMOT.NS",
    "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS",
    "ITC.NS", "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS",
    "KOTAKBANK.NS", "LTIM.NS", "LT.NS", "M&M.NS",
    "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SHRIRAMFIN.NS",
    "SBIN.NS", "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS",
    "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS", "TITAN.NS",
    "ULTRACEMCO.NS", "WIPRO.NS"
]

# ── 1. Download 5 years of data ──────────────────────────────────────────────
print("Downloading data...")
df = yf.download(nifty50, period="5y", interval="1d")
close = df["Close"]
close.columns = [c.replace(".NS", "") for c in close.columns]

# ── 2. Resample to month-end prices ──────────────────────────────────────────
monthly = close.resample("ME").last()

# ── 3. Calculate 12-month trailing return for each stock each month ───────────
momentum = monthly.pct_change(12)  # return over last 12 months

# ── 4. Strategy: rank stocks, pick top 10, equal weight, rebalance monthly ───
monthly_returns = monthly.pct_change()  # 1-month forward return

portfolio_returns = []
portfolio_dates   = []
selected_stocks   = []

for i in range(12, len(monthly) - 1):
    # Rank by 12-month momentum at month i
    scores = momentum.iloc[i].dropna()
    top10  = scores.nlargest(10).index.tolist()

    # Equal weight return next month
    next_month_return = monthly_returns.iloc[i + 1][top10].mean()

    portfolio_returns.append(next_month_return)
    portfolio_dates.append(monthly.index[i + 1])
    selected_stocks.append(top10)

# ── 5. Build equity curve ────────────────────────────────────────────────────
results = pd.DataFrame({
    "date":   portfolio_dates,
    "return": portfolio_returns
}).set_index("date")

results["equity_curve"]   = (1 + results["return"]).cumprod()
results["nifty50_return"] = monthly_returns.mean(axis=1).reindex(results.index)
results["nifty50_curve"]  = (1 + results["nifty50_return"]).cumprod()

# ── 6. Performance metrics ───────────────────────────────────────────────────
total_return   = results["equity_curve"].iloc[-1] - 1
nifty_return   = results["nifty50_curve"].iloc[-1] - 1
annual_return  = (1 + total_return) ** (12 / len(results)) - 1
annual_vol     = results["return"].std() * np.sqrt(12)
sharpe         = annual_return / annual_vol
max_dd         = (results["equity_curve"] / results["equity_curve"].cummax() - 1).min()

print("\n── Strategy Performance ──────────────────────")
print(f"Total return:       {total_return:.1%}")
print(f"Nifty 50 return:    {nifty_return:.1%}")
print(f"Annual return:      {annual_return:.1%}")
print(f"Annual volatility:  {annual_vol:.1%}")
print(f"Sharpe ratio:       {sharpe:.2f}")
print(f"Max drawdown:       {max_dd:.1%}")

# ── 7. Plot equity curve ─────────────────────────────────────────────────────
plt.figure(figsize=(12, 5))
plt.plot(results["equity_curve"],  label="Momentum strategy (top 10)", linewidth=2)
plt.plot(results["nifty50_curve"], label="Nifty 50 equal weight",      linewidth=2, linestyle="--")
plt.title("Nifty 50 Momentum Strategy vs Benchmark")
plt.ylabel("Growth of ₹1")
plt.xlabel("Date")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("momentum_strategy.png", dpi=150)
plt.show()
print("\nChart saved as momentum_strategy.png")

# ── 8. Show current month's top 10 picks ────────────────────────────────────
latest_top10 = selected_stocks[-1]
latest_scores = momentum.iloc[-2][latest_top10].sort_values(ascending=False)
print("\n── Current top 10 momentum stocks ───────────")
print(latest_scores.apply(lambda x: f"{x:.1%}"))