import pandas as pd

def get_coin_metadata() -> dict:
    return {
        "targets": [{"symbol": "SOL", "timeframe": "1H"}],
        "anchors": [
            {"symbol": "BTC", "timeframe": "1H"},
            {"symbol": "ETH", "timeframe": "4H"}
        ]
    }

def generate_signals(anchor_df: pd.DataFrame, target_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(target_df, anchor_df, on="timestamp", how="inner")

    # Lag features
    df["lag_close"] = df["Close"].shift(1)
    df["ret_target"] = df["Close"].pct_change()
    df["ret_lag_1"] = df["Close"].pct_change(periods=1)
    df["ret_lag_2"] = df["Close"].pct_change(periods=2)

    # Anchor returns
    df["ret_BTC"] = df["close_BTC_1h"].pct_change()
    df["ret_ETH"] = df["close_ETH_4h"].pct_change(fill_method=None)


    # Rolling features
    df["rolling_mean_3h"] = df["Close"].rolling(window=3).mean()
    df["rolling_std_6h"] = df["Close"].rolling(window=6).std()

    # Alpha logic
    df["alpha"] = df["ret_target"] - 0.5 * (df["ret_BTC"] + df["ret_ETH"])
    df["signal"] = "HOLD"
    df["position_size"] = 0.0

    df.loc[df["alpha"] > 0.002, ["signal", "position_size"]] = ["BUY", 0.5]
    df.loc[df["alpha"] < -0.002, ["signal", "position_size"]] = ["SELL", 0.5]

    return df[["timestamp", "signal", "position_size"]].assign(symbol="SOL")
