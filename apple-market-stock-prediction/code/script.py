# Install the Yahoo Finance library for fetching stock data
!pip install --upgrade finance

#Import necessary libraries
import yfinance as yf
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

#Data collection using yfinance

def download_data_with_retry(ticker, start, end, interval, max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            data = yf.download(ticker, start=start, end=end, interval=interval)
            

            print("Download successful!")
            return data
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    print("All retry attempts failed.")
    return None

# Define parameters
ticker = 'AAPL'
start_date = '2004-01-01'
end_date = '2024-01-01'
interval = '1d'

# Download data with retry
data = download_data_with_retry(ticker, start_date, end_date, interval) 

#Check the total record
if data is not None:
    print(f"Number of records downloaded: {len(data)}")
else:
    print("Data download failed.")

#Rename the columns
# Check if the DataFrame has MultiIndex columns
if isinstance(data.columns, pd.MultiIndex):
    # Flatten the MultiIndex (dropping the first level if needed)
    data.columns = data.columns.droplevel(0)

# After flattening, ensure the number of columns matches the number of new column names
data.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'OtherColumn']

#Save the file to CSV format
data.to_csv('AAPL_stock_data.csv')

#Data Processing 

data = pd.read_csv('AAPL_stock_data.csv', parse_dates=['Date'], index_col='Date')
print(data.info())  # Check for missing values, column types, etc.

print(data.isnull().sum())
data = data.ffill()

# Detect and remove outliers (using IQR as an example)
Q1 = data['Close'].quantile(0.25)
Q3 = data['Close'].quantile(0.75)
IQR = Q3 - Q1
data = data[(data['Close'] >= (Q1 - 1.5 * IQR)) & (data['Close'] <= (Q3 + 1.5 * IQR))]

# Scaling
scaler = StandardScaler()
scaled_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)



# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title("Feature Correlation Matrix")
plt.show()

# Rolling volatility
data['Volatility'] = data['Close'].rolling(window=20).std()
plt.figure(figsize=(14, 6))
plt.plot(data['Volatility'], label='20-day Volatility')
plt.title("Rolling Volatility")
plt.legend()
plt.show()
