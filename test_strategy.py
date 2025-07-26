import pandas as pd
from src.strategy import PairwiseAlphaStrategy

# Load pre-downloaded data
df_target = pd.read_csv("data/candles_target.csv")
df_anchor = pd.read_csv("data/candles_anchor.csv")

# Initialize strategy
strategy = PairwiseAlphaStrategy()
strategy.initialize(df_target, df_anchor)

# Run a test prediction
sample_timestamp = df_target["timestamp"].iloc[100]
signal = strategy.predict(sample_timestamp)
print(f"Signal at {sample_timestamp}: {signal}")
