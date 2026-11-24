import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("visuals", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

EMERALD = "#065F46"
COBALT = "#2563EB"
TEAL = "#0D9488"
CRIMSON = "#DC2626"
AMBER = "#D97706"
SLATE = "#64748B"

df = pd.read_csv("data/processed/sp500_cleaned.csv", parse_dates=["date"])
summary = pd.read_csv("data/processed/stock_kpi_summary.csv")

full_summary = summary[summary["is_complete_history"]].copy()
focus_tickers = ["NVDA", "AMZN", "AAPL", "BAC", "JNJ", "CHK"]
focus_df = df[df["symbol"].isin(focus_tickers)].copy()
focus_summary = (
    full_summary[full_summary["symbol"].isin(focus_tickers)]
    .set_index("symbol")
    .loc[focus_tickers]
    .reset_index()
)
focus_summary.to_csv("data/processed/focus_stocks_comparison.csv", index=False)

palette = {"NVDA": EMERALD, "AMZN": COBALT, "AAPL": TEAL, "BAC": "#7C3AED", "JNJ": AMBER, "CHK": CRIMSON}

# CHART 1: Top 10 Stocks by Total Return (%)
top10_ret = full_summary.nlargest(10, "total_return_pct").sort_values("total_return_pct")
fig, ax = plt.subplots(figsize=(10, 5.5))
colors = [COBALT if s in focus_tickers else EMERALD for s in top10_ret["symbol"]]
bars = ax.barh(top10_ret["symbol"], top10_ret["total_return_pct"], color=colors)
ax.set_title("Top 10 S&P 500 Stocks by Cumulative Return (2014–2017)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Cumulative Return (%)")
for bar in bars:
    w = bar.get_width()
    ax.text(w + 15, bar.get_y() + bar.get_height()/2, f"{w:,.1f}%", va="center", fontsize=9, fontweight="bold")
ax.set_xlim(0, top10_ret["total_return_pct"].max() * 1.15)
plt.tight_layout()
plt.savefig("visuals/01_top10_total_returns.png", dpi=300)
plt.close()

# CHART 2: Normalized Price Growth
fig, ax = plt.subplots(figsize=(11, 5.5))
for sym in focus_tickers:
    sub = focus_df[focus_df["symbol"] == sym].sort_values("date").copy()
    sub["indexed_price"] = (sub["close"] / sub["close"].iloc[0]) * 100
    ax.plot(sub["date"], sub["indexed_price"], label=f"{sym} ({sub['indexed_price'].iloc[-1]-100:+.0f}%)", linewidth=2, color=palette[sym])
ax.axhline(100, color="black", linestyle="--", linewidth=0.8, alpha=0.6)
ax.set_title("Normalized Growth of $100 Invested Across 6 Focus Stocks (2014–2017)", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Indexed Value (Jan 2, 2014 = 100)")
ax.legend(frameon=False, loc="upper left")
plt.tight_layout()
plt.savefig("visuals/02_focus_stocks_normalized_growth.png", dpi=300)
plt.close()

# CHART 3: Risk vs. Return Scatter
fig, ax = plt.subplots(figsize=(9.5, 5.5))
ax.scatter(full_summary["volatility_pct"], full_summary["total_return_pct"], alpha=0.25, color=SLATE, label="Other S&P 500 Stocks")
for _, row in focus_summary.iterrows():
    ax.scatter(row["volatility_pct"], row["total_return_pct"], color=palette[row["symbol"]], s=110, edgecolor="black", zorder=5)
    ax.annotate(row["symbol"], (row["volatility_pct"] + 0.06, row["total_return_pct"] + 15), fontweight="bold", fontsize=10)
ax.axhline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.6)
ax.set_title("Risk vs. Return Profile: Daily Volatility (%) vs. Cumulative Return (%)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Historical Daily Volatility (Std Dev of Daily Return %)")
ax.set_ylabel("Cumulative Return 2014–2017 (%)")
plt.tight_layout()
plt.savefig("visuals/03_risk_vs_return_scatter.png", dpi=300)
plt.close()

# CHART 4: AAPL Closing Price with Moving Averages
aapl = focus_df[focus_df["symbol"] == "AAPL"].sort_values("date")
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(aapl["date"], aapl["close"], color=SLATE, alpha=0.55, linewidth=1.2, label="Daily Close")
ax.plot(aapl["date"], aapl["ma_20"], color=COBALT, linewidth=1.8, label="20-Day Moving Average")
ax.plot(aapl["date"], aapl["ma_50"], color=EMERALD, linewidth=2.0, label="50-Day Moving Average")
ax.set_title("AAPL Closing Price & Moving Average Trends (2014–2017)", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Closing Price (USD)")
ax.legend(frameon=False, loc="upper left")
plt.tight_layout()
plt.savefig("visuals/04_aapl_moving_averages.png", dpi=300)
plt.close()

# CHART 5: Daily Return Distribution Boxplot
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(
    data=focus_df.dropna(subset=["daily_return_pct"]),
    x="symbol",
    y="daily_return_pct",
    hue="symbol",
    order=focus_tickers,
    palette=palette,
    legend=False,
    fliersize=2,
    ax=ax
)
ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
ax.set_title("Daily Percentage Return Distribution & Tail Risk Across 6 Focus Stocks", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Stock Symbol")
ax.set_ylabel("Daily Return (%)")
plt.tight_layout()
plt.savefig("visuals/05_daily_return_distributions.png", dpi=300)
plt.close()

# CHART 6: Average Daily Trading Volume
vol_sorted = focus_summary.sort_values("avg_daily_volume", ascending=True)
fig, ax = plt.subplots(figsize=(9.5, 5))
bars = ax.barh(vol_sorted["symbol"], vol_sorted["avg_daily_volume"] / 1e6, color=[palette[s] for s in vol_sorted["symbol"]])
ax.set_title("Average Daily Trading Volume Across 6 Focus Stocks (Millions of Shares)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Average Daily Volume (Millions of Shares)")
for bar in bars:
    w = bar.get_width()
    ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.2f}M", va="center", fontsize=9.5, fontweight="bold")
ax.set_xlim(0, (vol_sorted["avg_daily_volume"].max() / 1e6) * 1.15)
plt.tight_layout()
plt.savefig("visuals/06_focus_stocks_avg_volume.png", dpi=300)
plt.close()

print("SUCCESS! Overwrote all 6 PNG charts with Emerald & Cobalt palette.")