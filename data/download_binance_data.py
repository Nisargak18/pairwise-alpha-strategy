import os
import time
import datetime
import pandas as pd
import requests

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def to_milliseconds(dt):
    return int(dt.timestamp() * 1000)

def fetch_ohlcv_monthly(symbol, interval, start_date, end_date):
    """Fetch OHLCV data month-by-month to avoid API errors."""
    url = "https://api.binance.com/api/v3/klines"
    df_all = pd.DataFrame()

    current = start_date
    while current < end_date:
        month_end = (current.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        if month_end > end_date:
            month_end = end_date

        start_ms = to_milliseconds(current)
        end_ms = to_milliseconds(month_end)

        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_ms,
            "endTime": end_ms,
            "limit": 1000
        }

        print(f"Fetching {symbol} from {current.date()} to {month_end.date()}")
        response = requests.get(url, params=params)
        try:
            data = response.json()
        except:
            data = []

        if not data or isinstance(data, dict) and data.get("code"):
            print("   No data or error from Binance API:", data)
            time.sleep(1)
            current = month_end
            continue

        df = pd.DataFrame(data)
        df_all = pd.concat([df_all, df], ignore_index=True)
        time.sleep(0.3)
        current = month_end

    return df_all

def format_dataframe(df, symbol=None, interval=None, rename_cols=False):
    if df.empty:
        return df

    df.columns = [
        "Open Time", "Open", "High", "Low", "Close", "Volume",
        "Close Time", "Quote Asset Volume", "Number of Trades",
        "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
    ]
    df = df[["Open Time", "Open", "High", "Low", "Close", "Volume"]]
    df.loc[:, "Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
    df = df.rename(columns={"Open Time": "timestamp"})

    if rename_cols and symbol and interval:
        df = df.rename(columns={
            "Open": f"open_{symbol}_{interval}",
            "High": f"high_{symbol}_{interval}",
            "Low": f"low_{symbol}_{interval}",
            "Close": f"close_{symbol}_{interval}",
            "Volume": f"volume_{symbol}_{interval}",
        })
    return df

def get_coin_metadata():
    return {
        "target": {"symbol": "SOL", "interval": "1h"},
        "anchors": [
            {"symbol": "BTC", "interval": "1h"},
            {"symbol": "ETH", "interval": "4h"}
        ]
    }

if __name__ == "__main__":
    metadata = get_coin_metadata()
    start_date = datetime.datetime(2024, 6, 1)
    end_date = datetime.datetime(2025, 6, 1)

    # === Target Coin ===
    target = metadata["target"]
    print(f"\n Downloading TARGET: {target['symbol']}USDT @ {target['interval']}")
    df_target = fetch_ohlcv_monthly(
        symbol=target["symbol"] + "USDT",
        interval=target["interval"],
        start_date=start_date,
        end_date=end_date
    )

    if not df_target.empty:
        df_target = format_dataframe(df_target)
        df_target.to_csv(f"{DATA_DIR}/candles_target.csv", index=False)
        print(f" Saved to {DATA_DIR}/candles_target.csv")

        # Volume check
        df_target["Close"] = df_target["Close"].astype(float)
        df_target["Volume"] = df_target["Volume"].astype(float)
        df_target["VolumeUSD"] = df_target["Close"] * df_target["Volume"]
        df_target["date"] = df_target["timestamp"].dt.date
        avg_daily_volume_usd = df_target.groupby("date")["VolumeUSD"].sum().mean()
        print(f" Avg daily volume: ${avg_daily_volume_usd:,.2f}")
        if avg_daily_volume_usd < 5_000_000:
            print(" Volume too low. Try a different target coin.")
        else:
            print(" Volume rule satisfied.")
    else:
        print(" No target data fetched. Exiting.")

    # === Anchor Coins ===
    df_all_anchors = pd.DataFrame()
    for anchor in metadata["anchors"]:
        print(f"\n Downloading ANCHOR: {anchor['symbol']}USDT @ {anchor['interval']}")
        df_anchor = fetch_ohlcv_monthly(
            symbol=anchor["symbol"] + "USDT",
            interval=anchor["interval"],
            start_date=start_date,
            end_date=end_date
        )

        if df_anchor.empty:
            print(f"⚠️ Skipping {anchor['symbol']}, no data.")
            continue

        df_anchor = format_dataframe(df_anchor, anchor["symbol"], anchor["interval"], rename_cols=True)

        if df_all_anchors.empty:
            df_all_anchors = df_anchor
        else:
            df_all_anchors = pd.merge(df_all_anchors, df_anchor, on="timestamp", how="outer")

    if not df_all_anchors.empty:
        df_all_anchors = df_all_anchors.sort_values("timestamp")
        df_all_anchors.to_csv(f"{DATA_DIR}/candles_anchor.csv", index=False)
        print(f"Anchors saved to {DATA_DIR}/candles_anchor.csv")
    else:
        print("No anchor data saved.")
