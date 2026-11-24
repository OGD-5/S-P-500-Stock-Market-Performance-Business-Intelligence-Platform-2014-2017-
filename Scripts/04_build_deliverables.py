import os
import json

os.makedirs("notebooks", exist_ok=True)
os.makedirs("docs", exist_ok=True)

print("1. Generating Jupyter Notebook (notebooks/SP500_Market_Intelligence.ipynb)...")

notebook_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# S&P 500 Stock Market Performance & Business Intelligence (2014–2017)\n",
            "**Analyst:** Olabode Goodness Daniel (OGD Analytics) | **Track:** Data Analytics (Track A) | **Programme:** AnalystLab Africa Experience Lab\n",
            "\n",
            "## 1. Business Problem & Objectives\n",
            "Financial researchers and market analysts need structured, validated insights across 505 S&P 500 equities from 2014 to 2017 (497,472 daily trading records). Rather than relying on raw nominal share prices—which distort cross-company comparisons—this notebook inspects data quality, engineers per-symbol return and volatility metrics, evaluates market trends across 8 core business questions, and compares 6 representative focus stocks (`NVDA`, `AMZN`, `AAPL`, `BAC`, `JNJ`, `CHK`).\n",
            "\n",
            "**Key Scope & Historical Limitations:**\n",
            "- Dataset covers **January 2, 2014 to December 29, 2017** (1,007 trading days) and does not reflect current market prices.\n",
            "- Prices reflect unadjusted historical trading records without explicit dividend or split-adjustment columns.\n",
            "- Historical performance and volatility describe past behavior and do not guarantee future returns."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "plt.rcParams['figure.facecolor'] = 'white'\n",
            "plt.rcParams['axes.spines.top'] = False\n",
            "plt.rcParams['axes.spines.right'] = False\n",
            "\n",
            "raw_df = pd.read_csv('../data/raw/S&P 500 Stock Prices 2014-2017.csv')\n",
            "print(f'Raw Shape: {raw_df.shape[0]:,} rows x {raw_df.shape[1]} columns')\n",
            "raw_df.head()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Data Inspection & Quality Audit\n",
            "We inspect data types, date coverage, duplicate symbol-date pairs, missing OHLC values, zero-volume records, and incomplete stock histories."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "df = raw_df.copy()\n",
            "df['date'] = pd.to_datetime(df['date'])\n",
            "df = df.sort_values(['symbol', 'date']).reset_index(drop=True)\n",
            "\n",
            "print('Missing values per column:\\n', df.isnull().sum())\n",
            "print('Duplicate symbol-date pairs:', df.duplicated(subset=['symbol', 'date']).sum())\n",
            "print('Zero-volume rows:', (df['volume'] == 0).sum())\n",
            "print('Date range:', df['date'].min().date(), 'to', df['date'].max().date())\n",
            "print('Unique symbols:', df['symbol'].nunique(), '| Trading days:', df['date'].nunique())\n",
            "\n",
            "symbol_counts = df.groupby('symbol')['date'].count()\n",
            "print('Stocks with full 1,007 days:', (symbol_counts == 1007).sum())\n",
            "print('Stocks with partial history (< 1,007 days):', (symbol_counts < 1007).sum())"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Data Cleaning & Feature Engineering (Per Symbol)\n",
            "- Impute the 11 missing `open`/`high`/`low` cells using that trading day's intact `close` price (never `0`), while preserving quality flags (`had_missing_ohl`, `is_zero_volume`).\n",
            "- Compute `year`, `month`, `quarter`, `daily_price_change`, `daily_return_pct`, `daily_trading_range`, and 20-day / 50-day moving averages strictly grouped by `symbol`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "df['had_missing_ohl'] = df[['open', 'high', 'low']].isnull().any(axis=1)\n",
            "df['is_zero_volume'] = df['volume'] == 0\n",
            "for col in ['open', 'high', 'low']:\n",
            "    df[col] = df[col].fillna(df['close'])\n",
            "\n",
            "df['year'] = df['date'].dt.year\n",
            "df['month'] = df['date'].dt.month\n",
            "df['quarter'] = 'Q' + df['date'].dt.quarter.astype(str)\n",
            "df['daily_price_change'] = df.groupby('symbol')['close'].diff()\n",
            "df['daily_return_pct'] = df.groupby('symbol')['close'].pct_change() * 100\n",
            "df['daily_trading_range'] = df['high'] - df['low']\n",
            "df['ma_20'] = df.groupby('symbol')['close'].transform(lambda s: s.rolling(20, min_periods=1).mean())\n",
            "df['ma_50'] = df.groupby('symbol')['close'].transform(lambda s: s.rolling(50, min_periods=1).mean())\n",
            "df['trading_days_count'] = df.groupby('symbol')['date'].transform('count')\n",
            "df['is_complete_history'] = df['trading_days_count'] == 1007\n",
            "\n",
            "summary = pd.read_csv('../data/processed/stock_kpi_summary.csv')\n",
            "full_summary = summary[summary['is_complete_history']].copy()\n",
            "full_summary.sort_values('total_return_pct', ascending=False).head(10)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Comparative Analysis of 6 Focus Stocks & Validation\n",
            "We compare `NVDA`, `AMZN`, `AAPL`, `BAC`, `JNJ`, and `CHK` across cumulative return, daily volatility, closing price range, and average trading volume, followed by independent calculation verification."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "focus_tickers = ['NVDA', 'AMZN', 'AAPL', 'BAC', 'JNJ', 'CHK']\n",
            "focus_comp = full_summary[full_summary['symbol'].isin(focus_tickers)].set_index('symbol').loc[focus_tickers]\n",
            "print(focus_comp[['start_close', 'end_close', 'min_close', 'max_close', 'total_return_pct', 'volatility_pct', 'avg_daily_volume']].to_string())\n",
            "\n",
            "# Independent Validation Check\n",
            "aapl = df[df['symbol'] == 'AAPL'].head(3)\n",
            "manual_ret = ((aapl.iloc[1]['close'] - aapl.iloc[0]['close']) / aapl.iloc[0]['close']) * 100\n",
            "assert np.isclose(manual_ret, aapl.iloc[1]['daily_return_pct']), 'Return mismatch!'\n",
            "print(f'\\nValidation Passed: AAPL 2014-01-03 Daily Return = {manual_ret:.6f}%')"
        ]
    }
]

nb_json = {
    "cells": notebook_cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.15"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("notebooks/SP500_Market_Intelligence.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb_json, f, indent=2)

print("2. Generating KPI Definition Sheet (docs/KPI_Definition_Sheet.md)...")
kpi_doc = """# KPI Definition Sheet — S&P 500 Market Intelligence (2014–2017)

| Metric / KPI Name | Formula / Calculation Method | Unit | Business & Analytical Interpretation |
| :--- | :--- | :---: | :--- |
| **Daily Price Change** | `Close_t - Close_(t-1)` (computed per symbol) | USD ($) | Measures absolute single-day dollar movement in share price. |
| **Daily Percentage Return** | `((Close_t - Close_(t-1)) / Close_(t-1)) * 100` | % | Normalizes daily performance across high-priced and low-priced stocks for fair comparison. |
| **Cumulative Return (2014–2017)** | `((Close_end - Close_start) / Close_start) * 100` | % | Measures total percentage appreciation or drawdown across the full 1,007-day observation window. |
| **Historical Volatility** | Sample standard deviation `s` of `Daily Percentage Return` per stock | % | Quantifies daily price risk and return dispersion; higher values indicate wider daily swings. |
| **Daily Trading Range** | `High_t - Low_t` | USD ($) | Captures intraday price spread between session peak and trough. |
| **20-Day & 50-Day Moving Averages** | Rolling arithmetic mean of `Close` over 20 and 50 trading days per stock | USD ($) | Smooths short-term daily noise to reveal medium-term trend direction and support/resistance. |
| **Average Daily Volume** | `Sum(Volume) / Trading_Days` per stock | Shares | Measures average daily market liquidity and investor participation (not dollar turnover). |
"""
with open("docs/KPI_Definition_Sheet.md", "w", encoding="utf-8") as f:
    f.write(kpi_doc)

print("3. Generating Data Quality & Validation Report (docs/Data_Quality_and_Validation.md)...")
dq_doc = """# Data Quality Assessment & Independent Validation Report

## 1. Dataset Structural Audit
- **Source File:** `S&P 500 Stock Prices 2014-2017.csv` (preserved untouched in `data/raw/`)
- **Dimensions:** 497,472 records × 7 columns (`symbol`, `date`, `open`, `high`, `low`, `close`, `volume`)
- **Coverage:** 505 unique stock symbols across 1,007 distinct trading dates (`2014-01-02` to `2017-12-29`)
- **Duplicates & Non-Positive Prices:** 0 duplicate `(symbol, date)` records; 0 negative or zero price records (`close` min = $1.59, max = $2,049.00)

## 2. Identified Data-Quality Issues & Remediation
| Quality Issue | Audit Count | Affected Records / Details | Cleaning & Analytical Treatment |
| :--- | :---: | :--- | :--- |
| **Missing `open` prices** | 11 | `VRTX`, `REGN`, `WRK`, `DHR` (×2), `ES`, `O` (×2), `UA`, `FTV`, `BHF` | Imputed with that session's intact `close` price (never `0`); flagged via `had_missing_ohl = True`. |
| **Missing `high` & `low` prices** | 8 | Same 11 rows excluding `2015-07-17` (`DHR`, `ES`, `O`), which retained valid `high`/`low` | Imputed with that session's intact `close` price; `close` had 0 missing values so daily returns remained 100% intact. |
| **Zero-volume trading days** | 4 | `DHR` & `O` (`2016-01-12`), `UA` (`2016-04-07`), `FTV` (`2016-07-01`) | Retained with `is_zero_volume = True` flag for transparency. |
| **Incomplete stock histories** | 26 tickers | 479 tickers have all 1,007 days; 26 tickers have 18–995 days (e.g., `APTV`: 18, `DWDP`: 83) | Flagged via `is_complete_history`. Cross-stock rankings restrict comparisons to the 479 full-history tickers. |

## 3. Success Criteria & Independent Validation Evidence (Task 6)
1. **Zero Missing Values Post-Cleaning:** Verified `0` nulls across all core OHLCV fields in `data/processed/sp500_cleaned.csv`.
2. **Daily Return Formula Reconciliation (`AAPL`):** Manual check on `2014-01-03` (`close = $77.2828` vs. `2014-01-02 close = $79.0185`) yields `-2.196574%`, matching script output `-2.196574%` (`Match = True`).
3. **20-Day Moving Average Reconciliation (`AAPL`):** Manual arithmetic mean of first 20 closing prices (`$77.041060`) matches `ma_20` column (`$77.041060`, `Match = True`).
4. **Cumulative Return Reconciliation (`NVDA`):** Manual calculation from `$15.86` (`2014-01-02`) to `$193.50` (`2017-12-29`) yields `+1,120.0504%`, matching `stock_kpi_summary.csv` (`Match = True`).
5. **Interactive Filter Verification:** Verified stock symbol dropdowns (`NVDA`, `AMZN`, `AAPL`, `BAC`, `JNJ`, `CHK`) and date range sliders across Pages 2 and 4 of `SP500_Interactive_Dashboard.html`.
"""
with open("docs/Data_Quality_and_Validation.md", "w", encoding="utf-8") as f:
    f.write(dq_doc)

print("4. Generating Executive Summary (docs/Executive_Summary.md)...")
exec_doc = """# Executive Summary: S&P 500 Market Performance & Intelligence (2014–2017)

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
"""
with open("docs/Executive_Summary.md", "w", encoding="utf-8") as f:
    f.write(exec_doc)

print("5. Generating Project README (README.md)...")
readme_doc = """# S&P 500 Stock Market Performance & Business Intelligence Platform (2014–2017)

**Author:** Olabode Goodness Daniel (OGD Analytics)  
**Programme:** AnalystLab Africa — Experience Lab Internship Programme (Week 6, Track A: Data Analytics)  

## Project Overview
An end-to-end financial market analytics pipeline and 4-page interactive Plotly dashboard examining 497,472 daily stock records across 505 S&P 500 symbols from January 2, 2014 to December 29, 2017.

## Folder Structure
- `data/raw/` — Original `S&P 500 Stock Prices 2014-2017.csv` (untouched)
- `data/processed/` — Cleaned dataset (`sp500_cleaned.csv`), full KPI summary, and focus stocks comparison table
- `scripts/` — Reproducible Python scripts (`01_data_prep.py` through `04_build_deliverables.py`)
- `notebooks/` — `SP500_Market_Intelligence.ipynb`
- `visuals/` — 6 static PNG charts, dashboard screenshots, and `SP500_Interactive_Dashboard.html`
- `docs/` — `KPI_Definition_Sheet.md`, `Data_Quality_and_Validation.md`, and `Executive_Summary.md`

## Setup & Reproduction Instructions
1. Install required Python libraries:

       pip install pandas numpy matplotlib seaborn plotly jupyter

2. Run the pipeline sequentially from the project root folder:

       python scripts/01_data_prep.py
       python scripts/02_market_analysis.py
       python scripts/03_dashboard.py
       python scripts/04_build_deliverables.py

3. Open `visuals/SP500_Interactive_Dashboard.html` in any modern web browser to explore all 4 interactive dashboard pages.

## Key Assumptions & Limitations
- **Historical Coverage:** Covers 2014–2017 only; findings do not represent current stock prices or future guarantees.
- **Unadjusted Prices:** Dataset omits explicit dividend/split-adjustment columns; cumulative returns reflect raw historical close-to-close changes.
- **Currency & Volume:** All prices are denominated in USD; trading volume reflects share count rather than dollar turnover.
"""
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_doc)

print("\nSUCCESS! Created Jupyter Notebook, KPI Sheet, Data Quality Report, Executive Summary, and README.md!")