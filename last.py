# Code to obtain stock data using Pandas Datareader
# Select the start/end dates and ticker symbols
# Data is saved in a stock_data.csv file
tickers = ['AMZN', 'JPM', 'META', 'PG', 'GOOGL', 'CAT', 'PFE', 'EXC', 'DE', 'JNJ'] 
tickers = ['AMZN'] 

#!pip install pandas_datareader
#!pip install yfinance
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()

# Indicate the start and end dates
start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()

df = pdr.get_data_yahoo(tickers, start = start, end = end)
print(df)
df.to_csv('stock_data.csv')