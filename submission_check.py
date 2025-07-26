import pandas as pd
from strategy import get_coin_metadata, generate_signals

def main():
    try:
        # Load candle data
        df_target = pd.read_csv("data/candles_target.csv")
        df_anchor = pd.read_csv("data/candles_anchor.csv")
    except FileNotFoundError:
        print("Data files not found. Ensure candles_target.csv and candles_anchor.csv are in the data/ folder.")
        return

    try:
        signal_df = generate_signals(df_anchor, df_target)
        print(" Submission check passed.")
        print("Sample output:")
        print(signal_df.head())
    except Exception as e:
        print(" Error during signal generation:", e)

if __name__ == "__main__":
    main()
