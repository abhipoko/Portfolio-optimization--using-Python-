import yfinance as yf
import pandas as pd
import numpy as np
import os

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

# Create output folder
output_folder = "nifty50_ohlcv"
os.makedirs(output_folder, exist_ok=True)

print("Downloading Nifty 50 OHLCV data...")
df = yf.download(nifty50, period="1y", interval="1d")

success = []
failed = []

for ticker in nifty50:
    try:
        # Extract OHLCV for this ticker
        ticker_df = pd.DataFrame({
            "Open":   df["Open"][ticker],
            "High":   df["High"][ticker],
            "Low":    df["Low"][ticker],
            "Close":  df["Close"][ticker],
            "Volume": df["Volume"][ticker]
        })

        # Drop rows where all values are NaN
        ticker_df.dropna(how="all", inplace=True)

        if ticker_df.empty:
            failed.append(ticker)
            continue

        # Save to CSV
        filename = f"{output_folder}/{ticker.replace('.NS', '')}.csv"
        ticker_df.to_csv(filename)
        success.append(ticker)
        print(f"  saved: {filename}")

    except Exception as e:
        print(f"  failed: {ticker} — {e}")
        failed.append(ticker)

print(f"\nDone. {len(success)} files saved to '{output_folder}/'")
if failed:
    print(f"Failed tickers: {failed}")