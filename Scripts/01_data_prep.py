import os
import pandas as pd
import numpy as np

# Ensure output folders exist
os.makedirs("data/processed", exist_ok=True)
os.makedirs("docs", exist_ok=True)

print("1. Loading raw S&P 500 dataset...")
raw_path = "data/raw/S&P 500 Stock Prices 2014-2017.csv"
df = pd.read_csv(raw_path)

# Convert date to proper datetime format and sort chronologically per symbol
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["symbol", "date"]).reset_index(drop=True)

print("2. Flagging data-quality issues and cleaning missing prices...")
# Flag rows that had missing open/high/low (11 rows) or zero volume (4 rows)
df["had_missing_ohl"] = df[["open", "high", "low"]].isnull().any(axis=1)
df["is_zero_volume"] = df["volume"] == 0

# Impute missing open, high, low using that day's intact close price (never 0)
for col in ["open", "high", "low"]:
    df[col] = df[col].fillna(df["close"])

print("3. Engineering Track A analytical features per stock symbol...")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%b")
df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)

# Daily price change ($), daily percentage return (%), and daily trading range ($)
df["daily_price_change"] = df.groupby("symbol")["close"].diff()
df["daily_return_pct"] = df.groupby("symbol")["close"].pct_change() * 100
df["daily_trading_range"] = df["high"] - df["low"]

# 20-day and 50-day moving averages per symbol
df["ma_20"] = df.groupby("symbol")["close"].transform(
    lambda s: s.rolling(window=20, min_periods=1).mean()
)
df["ma_50"] = df.groupby("symbol")["close"].transform(
    lambda s: s.rolling(window=50, min_periods=1).mean()
)

# Track completeness of stock histories (1,007 max trading days)
df["trading_days_count"] = df.groupby("symbol")["date"].transform("count")
df["is_complete_history"] = df["trading_days_count"] == 1007

print("4. Building Stock Summary KPI Table...")
stock_summary = df.groupby("symbol").agg(
    trading_days=("date", "count"),
    start_date=("date", "min"),
    end_date=("date", "max"),
    start_close=("close", "first"),
    end_close=("close", "last"),
    min_close=("close", "min"),
    max_close=("close", "max"),
    avg_close=("close", "mean"),
    avg_daily_return_pct=("daily_return_pct", "mean"),
    volatility_pct=("daily_return_pct", "std"),
    total_volume=("volume", "sum"),
    avg_daily_volume=("volume", "mean"),
    max_daily_volume=("volume", "max"),
    min_daily_volume=("volume", "min"),
    avg_trading_range=("daily_trading_range", "mean"),
).reset_index()

stock_summary["total_return_pct"] = (
    (stock_summary["end_close"] - stock_summary["start_close"])
    / stock_summary["start_close"]
) * 100
stock_summary["is_complete_history"] = stock_summary["trading_days"] == 1007

# Save cleaned dataset and KPI summary table
df.to_csv("data/processed/sp500_cleaned.csv", index=False)
stock_summary.to_csv("data/processed/stock_kpi_summary.csv", index=False)

print("5. Running Independent Validation Checks (Task 6)...")
# Check 1: Manual calculation of AAPL's first daily return (2014-01-03 vs 2014-01-02)
aapl = df[df["symbol"] == "AAPL"].head(3)
manual_ret = ((aapl.iloc[1]["close"] - aapl.iloc[0]["close"]) / aapl.iloc[0]["close"]) * 100
script_ret = aapl.iloc[1]["daily_return_pct"]

# Check 2: Manual calculation of AAPL's 20-day moving average on day 20
aapl_20 = df[df["symbol"] == "AAPL"].iloc[:20]
manual_ma20 = aapl_20["close"].mean()
script_ma20 = aapl_20.iloc[19]["ma_20"]

# Check 3: Manual total return check for NVDA
nvda_row = stock_summary[stock_summary["symbol"] == "NVDA"].iloc[0]
manual_nvda_tot = ((nvda_row["end_close"] - nvda_row["start_close"]) / nvda_row["start_close"]) * 100

print("\n--- VALIDATION REPORT ---")
print(f"Total Rows: {len(df):,} | Total Columns: {df.shape[1]}")
print(f"Remaining Missing Values in Core Prices: {df[['open','high','low','close','volume']].isnull().sum().sum()}")
print(f"Check 1 (AAPL Daily Return): Manual = {manual_ret:.6f}% | Script = {script_ret:.6f}% | Match = {np.isclose(manual_ret, script_ret)}")
print(f"Check 2 (AAPL 20-Day MA):    Manual = ${manual_ma20:.6f} | Script = ${script_ma20:.6f} | Match = {np.isclose(manual_ma20, script_ma20)}")
print(f"Check 3 (NVDA Total Return): Manual = {manual_nvda_tot:.4f}% | Script = {nvda_row['total_return_pct']:.4f}% | Match = {np.isclose(manual_nvda_tot, nvda_row['total_return_pct'])}")
print("\nSUCCESS! Saved 'data/processed/sp500_cleaned.csv' and 'data/processed/stock_kpi_summary.csv'.")