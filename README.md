Proposal Title:
Deterministic Pairwise Alpha Strategy Using Time-Series Coin Returns




Objective:

The objective of this project is to develop a deterministic, rule-based trading strategy that generates buy, sell, or hold signals for a target cryptocurrency (SOL) by analyzing the historical relationships with selected anchor coins (BTC and ETH). The strategy aims to identify alpha opportunities based on relative return differentials between the target and anchor coins using only time-series data.

Background:

In volatile and highly correlated crypto markets, relationships between coins can uncover profitable trading opportunities. This project is a submission for the "Lunor Quest: PairWise Alpha Round 3", which challenges participants to build a reproducible and rule-based strategy for crypto asset trading using real Binance OHLCV (Open, High, Low, Close, Volume) data. The strategy does not involve any machine learning models and must operate entirely through statistical and deterministic logic.

Methodology:

1. Data Sources:

   * Target Coin: "SOL" (1H interval)
   * Anchor Coins: "BTC"(1H) and "ETH" (4H)
   * Data is aligned to a 1-hour frequency and includes price and volume information.

2. Feature Engineering:

   * Calculate percentage returns for each asset over time using the `pct_change()` method.
   * Compute an alpha signal:

     $$
     \text{alpha} = \text{ret\_SOL} - 0.5 \times (\text{ret\_BTC} + \text{ret\_ETH})
     $$

3. Signal Generation:

   * "BUY" signal if alpha > 0.002 (strong relative strength in SOL)
   * "SELL"signal if alpha < -0.002 (weak relative strength in SOL)
   * "HOLD" signal otherwise
   * Position size is fixed at 0.5 for BUY/SELL signals and 0.0 for HOLD.

4. Validation:

   * The strategy is tested using Lunor's local validator to ensure compliance with submission format, trading constraints, and performance expectations.



Tools and Technologies:

* Python 3.8+
* Pandas, NumPy
* Git/GitHub for version control
* Jupyter Notebook for EDA and preprocessing
* Command Line (Git Bash) for execution and deployment



Expected Outcomes:

* A working `strategy.py` file that meets Lunor Quest's technical requirements.
* A backtest-ready signal dataset.
* A GitHub repository containing:

  * Source code
  * Data samples
  * EDA and logic explanation notebook
  * ReadMe for usage and deployment



