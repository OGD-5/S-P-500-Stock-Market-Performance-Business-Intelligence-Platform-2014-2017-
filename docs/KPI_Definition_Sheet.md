# KPI Definition Sheet — S&P 500 Market Intelligence (2014–2017)

| Metric / KPI Name | Formula / Calculation Method | Unit | Business & Analytical Interpretation |
| :--- | :--- | :---: | :--- |
| **Daily Price Change** | `Close_t - Close_(t-1)` (computed per symbol) | USD ($) | Measures absolute single-day dollar movement in share price. |
| **Daily Percentage Return** | `((Close_t - Close_(t-1)) / Close_(t-1)) * 100` | % | Normalizes daily performance across high-priced and low-priced stocks for fair comparison. |
| **Cumulative Return (2014–2017)** | `((Close_end - Close_start) / Close_start) * 100` | % | Measures total percentage appreciation or drawdown across the full 1,007-day observation window. |
| **Historical Volatility** | Sample standard deviation `s` of `Daily Percentage Return` per stock | % | Quantifies daily price risk and return dispersion; higher values indicate wider daily swings. |
| **Daily Trading Range** | `High_t - Low_t` | USD ($) | Captures intraday price spread between session peak and trough. |
| **20-Day & 50-Day Moving Averages** | Rolling arithmetic mean of `Close` over 20 and 50 trading days per stock | USD ($) | Smooths short-term daily noise to reveal medium-term trend direction and support/resistance. |
| **Average Daily Volume** | `Sum(Volume) / Trading_Days` per stock | Shares | Measures average daily market liquidity and investor participation (not dollar turnover). |
