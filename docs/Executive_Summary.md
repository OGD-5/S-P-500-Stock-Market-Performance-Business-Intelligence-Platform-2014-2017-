# Executive Summary: S&P 500 Market Performance & Intelligence (2014–2017)

## 1. Business Problem & Purpose
Financial analysts evaluating historical equity markets face two core traps: comparing raw share prices instead of normalized percentage returns, and overlooking partial trading histories across index constituents. This project delivers a validated analytical pipeline and 4-page interactive Plotly dashboard covering 497,472 trading records across 505 S&P 500 tickers (2014–2017) to support equity benchmarking, risk-return profiling, and liquidity analysis.

## 2. Key Analytical Findings
1. **High Nominal Price Does Not Equal Highest Percentage Return:** Priceline (`PCLN`) reached the dataset's highest closing price (**$2,049.00** on Aug 8, 2017) and largest single-day dollar drop (**-$257.28** on Nov 7, 2017), yet delivered a **+51.71%** cumulative return—far behind lower-priced semiconductor leader **NVIDIA (`NVDA`)**, which surged **+1,120.05%** (`$15.86` to `$193.50`).
2. **Broad Multi-Year Bull Trend with a 2015 Pause:** Across the 479 full-history stocks, mean closing prices rose **+29.3%** from **$76.63** (2014) to **$99.12** (2017), punctuated by flat performance in 2015 (mean daily return `-0.0013%`) before accelerating in 2016–2017.
3. **Volatility Does Not Guarantee Positive Return:** Chesapeake Energy (`CHK`) recorded the highest daily volatility among full-history stocks (**4.55%** daily return std dev) alongside the worst cumulative drawdown (**-85.12%**), whereas Johnson & Johnson (`JNJ`) compounded **+53.49%** at just **0.89%** daily volatility.
4. **Liquidity Concentrates in Mega-Cap Financials & Tech:** Bank of America (`BAC`) led total trading volume with **89.99 billion shares** (`89.36M` daily avg), nearly double second-place Apple (`AAPL`, **45.49 billion shares**).
5. **Trading Volume Tracks Price Move Magnitude, Not Direction:** Across all 6 focus stocks, Pearson correlation between daily volume and signed daily return is near zero (`-0.07` to `+0.14`), whereas correlation between volume and **absolute** daily return size is strongly positive (**+0.49 to +0.74**).

## 3. Actionable Recommendations
1. **Standardize Equity Screening on Risk-Adjusted Percentage Returns:** Investment research teams should rank candidate stocks using cumulative/annualized percentage returns paired with daily volatility (`return-to-volatility` ratio) rather than nominal share price or unadjusted volatility. *Evidence: `NVDA` (+1,120.05% at 2.37% volatility) vs. `CHK` (-85.12% at 4.55% volatility).*
2. **Enforce Complete-History Filtering Before Benchmark Comparisons:** Analysts building multi-year peer benchmarks must filter out partial-history tickers (26 of 505 symbols, such as `APTV` with 18 trading days) to prevent distorted cumulative return and volume comparisons. *Evidence: Data-quality audit identifying 479 complete vs. 26 partial tickers.*
3. **Use Volume Spikes as Event-Driven Volatility Alerts, Not Directional Signals:** Risk-monitoring workflows should flag abnormal daily volume surges as indicators of heightened intraday price range (`High - Low`) rather than bullish or bearish directional triggers. *Evidence: Strong positive correlation (`r = +0.49` to `+0.74`) between volume and `|Daily Return %|` across focus stocks.*

*Disclaimer: All findings reflect historical S&P 500 data from 2014–2017 and do not constitute current market quotes or guarantees of future investment performance.*
