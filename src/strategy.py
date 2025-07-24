import pandas as pd

class PairwiseAlphaStrategy:
    def __init__(self):
        self.df_target = None
        self.df_anchor = None
        self.signal = None

    def get_coin_metadata(self):
        return {
            "target": {"symbol": "SOL", "interval": "1h"},
            "anchors": [
                {"symbol": "BTC", "interval": "1h"},
                {"symbol": "ETH", "interval": "4h"}
            ]
        }

    def initialize(self, candles_target: pd.DataFrame, candles_anchor: pd.DataFrame):
        self.df_target = candles_target.copy()
        self.df_anchor = candles_anchor.copy()

        # Ensure timestamp is datetime
        self.df_target["timestamp"] = pd.to_datetime(self.df_target["timestamp"])
        self.df_anchor["timestamp"] = pd.to_datetime(self.df_anchor["timestamp"])

        # Merge target and anchor data
        df = pd.merge(self.df_target, self.df_anchor, on="timestamp", how="inner")

        # Calculate a simple alpha signal: if SOL outperforms BTC and ETH
        df["ret_SOL"] = df["close"] = df["Close"].astype(float).pct_change()
        df["ret_BTC"] = df["close_BTC_1h"].astype(float).pct_change()
        df["ret_ETH"] = df["close_ETH_4h"].astype(float).pct_change()

        df["alpha"] = df["ret_SOL"] - 0.5 * (df["ret_BTC"] + df["ret_ETH"])

        # Scale alpha between -1 and +1
        df["signal"] = df["alpha"].clip(-1, 1).fillna(0)

        self.signal = df[["timestamp", "signal"]].set_index("timestamp")

    def predict(self, timestamp: str) -> float:
        timestamp = pd.to_datetime(timestamp)

        if timestamp in self.signal.index:
            return float(self.signal.loc[timestamp, "signal"])
        else:
            return 0.0  # Neutral if no data
