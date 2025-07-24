import requests
import pandas as pd
import time
import datetime

def fetch_ohlcv(symbol, interval, start_time, end_time):
    url = 'https://api.binance.com/api/v3/klines'
    df = pd.DataFrame()
    while start_time < end_time:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': min(start_time + 1000 * 60 * 60 * 500, end_time),
            'limit': 500
        }
        resp = requests.get(url, params=params)
        data = resp.json()
        if not data:
            break
        df = pd.concat([df, pd.DataFrame(data)])
        start_time = data[-1][0] + 1
        time.sleep(0.5)
    return df

def to_milliseconds(dt):
    """Convert a datetime object to milliseconds since epoch."""
    return int(dt.timestamp() * 1000)

if __name__ == "__main__":
    # Define date range
    start_date = datetime.datetime(2025, 7, 1)
    end_date = datetime.datetime(2025, 8, 31)
    start_ms = to_milliseconds(start_date)
    end_ms = to_milliseconds(end_date)

    df = fetch_ohlcv('BTCUSDT', '1h', start_ms, end_ms)
    
    # Set proper column names
    df.columns = [
        "Open Time", "Open", "High", "Low", "Close", "Volume",
        "Close Time", "Quote Asset Volume", "Number of Trades",
        "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
    ]
    
    df.to_csv('BTCUSDT_1h_2025_07_to_08.csv', index=False)
    print("Data downloaded and saved to BTCUSDT_1h_2025_07_to_08.csv")
