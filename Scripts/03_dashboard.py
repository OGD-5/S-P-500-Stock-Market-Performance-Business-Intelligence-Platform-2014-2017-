import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

os.makedirs("visuals", exist_ok=True)

df = pd.read_csv("data/processed/sp500_cleaned.csv", parse_dates=["date"])
summary = pd.read_csv("data/processed/stock_kpi_summary.csv")

full_summary = summary[summary["is_complete_history"]].copy()
focus_tickers = ["NVDA", "AMZN", "AAPL", "BAC", "JNJ", "CHK"]
focus_df = df[df["symbol"].isin(focus_tickers)].sort_values(["symbol", "date"]).copy()
focus_summary = (
    full_summary[full_summary["symbol"].isin(focus_tickers)]
    .set_index("symbol")
    .loc[focus_tickers]
    .reset_index()
)

EMERALD = "#065F46"
COBALT = "#2563EB"
TEAL = "#0D9488"
CRIMSON = "#DC2626"
AMBER = "#D97706"
SLATE = "#64748B"
PALETTE = {"NVDA": EMERALD, "AMZN": COBALT, "AAPL": TEAL, "BAC": "#7C3AED", "JNJ": AMBER, "CHK": CRIMSON}

# Page 1 Chart A
top10 = full_summary.nlargest(10, "total_return_pct").sort_values("total_return_pct")
fig_p1_a = go.Figure(
    go.Bar(
        x=top10["total_return_pct"],
        y=top10["symbol"],
        orientation="h",
        marker_color=[COBALT if s in focus_tickers else EMERALD for s in top10["symbol"]],
        text=[f"{v:,.1f}%" for v in top10["total_return_pct"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Return: %{x:,.2f}%<extra></extra>",
    )
)
fig_p1_a.update_layout(
    title=dict(text="Top 10 S&P 500 Stocks by Cumulative Return (2014–2017)", font=dict(size=15)),
    xaxis_title="Cumulative Return (%)",
    yaxis_title="Stock Symbol",
    template="plotly_white",
    height=420,
    margin=dict(l=60, r=60, t=55, b=45),
    xaxis=dict(range=[0, top10["total_return_pct"].max() * 1.18]),
)

# Page 1 Chart B
yearly = df[df["is_complete_history"]].groupby("year").agg(
    mean_close=("close", "mean"),
    median_close=("close", "median"),
    total_volume=("volume", "sum"),
).reset_index()

fig_p1_b = go.Figure()
fig_p1_b.add_trace(
    go.Bar(
        x=yearly["year"].astype(str),
        y=yearly["mean_close"],
        name="Mean Close ($)",
        marker_color=EMERALD,
        text=[f"${v:.2f}" for v in yearly["mean_close"]],
        textposition="outside",
    )
)
fig_p1_b.add_trace(
    go.Scatter(
        x=yearly["year"].astype(str),
        y=yearly["median_close"],
        name="Median Close ($)",
        mode="lines+markers+text",
        line=dict(color=COBALT, width=3),
        marker=dict(size=9),
        text=[f"${v:.2f}" for v in yearly["median_close"]],
        textposition="top center",
    )
)
fig_p1_b.update_layout(
    title=dict(text="Market Mean vs. Median Closing Price by Year", font=dict(size=15)),
    xaxis_title="Year",
    yaxis_title="Closing Price (USD)",
    template="plotly_white",
    height=420,
    yaxis=dict(range=[0, yearly["mean_close"].max() * 1.22]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# Page 2
fig_p2 = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    row_heights=[0.7, 0.3],
    subplot_titles=("OHLC Price & Moving Averages (20-Day & 50-Day)", "Daily Price Change ($)"),
)

for idx, sym in enumerate(focus_tickers):
    sub = focus_df[focus_df["symbol"] == sym]
    vis = idx == 0
    fig_p2.add_trace(
        go.Candlestick(
            x=sub["date"],
            open=sub["open"],
            high=sub["high"],
            low=sub["low"],
            close=sub["close"],
            name=f"{sym} OHLC",
            visible=vis,
            increasing_line_color=TEAL,
            decreasing_line_color=CRIMSON,
        ),
        row=1,
        col=1,
    )
    fig_p2.add_trace(
        go.Scatter(
            x=sub["date"],
            y=sub["ma_20"],
            name=f"{sym} 20-Day MA",
            line=dict(color=COBALT, width=1.8),
            visible=vis,
        ),
        row=1,
        col=1,
    )
    fig_p2.add_trace(
        go.Scatter(
            x=sub["date"],
            y=sub["ma_50"],
            name=f"{sym} 50-Day MA",
            line=dict(color=EMERALD, width=2.0),
            visible=vis,
        ),
        row=1,
        col=1,
    )
    bar_colors = [TEAL if v >= 0 else CRIMSON for v in sub["daily_price_change"].fillna(0)]
    fig_p2.add_trace(
        go.Bar(
            x=sub["date"],
            y=sub["daily_price_change"],
            name=f"{sym} Daily Change ($)",
            marker_color=bar_colors,
            visible=vis,
            showlegend=False,
        ),
        row=2,
        col=1,
    )

buttons_p2 = []
for idx, sym in enumerate(focus_tickers):
    vis_list = [False] * (len(focus_tickers) * 4)
    for k in range(4):
        vis_list[idx * 4 + k] = True
    buttons_p2.append(
        dict(
            label=sym,
            method="update",
            args=[
                {"visible": vis_list},
                {"title": f"Stock Price Performance & Moving Averages: {sym} (2014–2017)"},
            ],
        )
    )

fig_p2.update_layout(
    title="Stock Price Performance & Moving Averages: NVDA (2014–2017)",
    template="plotly_white",
    height=640,
    xaxis_rangeslider_visible=False,
    xaxis2_rangeslider_visible=True,
    xaxis2_rangeslider_thickness=0.06,
    updatemenus=[
        dict(
            active=0,
            buttons=buttons_p2,
            x=0.0,
            y=1.13,
            xanchor="left",
            yanchor="top",
            bgcolor="#F1F5F9",
            bordercolor="#CBD5E1",
        )
    ],
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1),
)
fig_p2.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig_p2.update_yaxes(title_text="Change ($)", row=2, col=1)

# Page 3
fig_p3_a = go.Figure()
for sym in focus_tickers:
    sub = focus_df[focus_df["symbol"] == sym].dropna(subset=["daily_return_pct"])
    fig_p3_a.add_trace(
        go.Box(
            y=sub["daily_return_pct"],
            name=sym,
            marker_color=PALETTE[sym],
            boxmean="sd",
        )
    )
fig_p3_a.update_layout(
    title=dict(text="Daily Return Distribution & Volatility Spread (6 Focus Stocks)", font=dict(size=15)),
    yaxis_title="Daily Return (%)",
    xaxis_title="Stock Symbol",
    template="plotly_white",
    height=430,
    showlegend=False,
)

fig_p3_b = go.Figure()
fig_p3_b.add_trace(
    go.Scatter(
        x=full_summary["volatility_pct"],
        y=full_summary["total_return_pct"],
        mode="markers",
        name="Other S&P 500 Stocks",
        marker=dict(color=SLATE, opacity=0.3, size=7),
        text=full_summary["symbol"],
        hovertemplate="<b>%{text}</b><br>Daily Volatility: %{x:.2f}%<br>Cumulative Return: %{y:.2f}%<extra></extra>",
    )
)
fig_p3_b.add_trace(
    go.Scatter(
        x=focus_summary["volatility_pct"],
        y=focus_summary["total_return_pct"],
        mode="markers+text",
        name="6 Focus Stocks",
        text=focus_summary["symbol"],
        textposition="top center",
        marker=dict(
            color=[PALETTE[s] for s in focus_summary["symbol"]],
            size=14,
            line=dict(color="black", width=1.5),
        ),
        hovertemplate="<b>%{text}</b><br>Daily Volatility: %{x:.2f}%<br>Cumulative Return: %{y:.2f}%<extra></extra>",
    )
)
fig_p3_b.update_layout(
    title=dict(text="Risk vs. Return: Volatility (%) vs. Cumulative Return (%)", font=dict(size=15)),
    xaxis_title="Historical Daily Volatility (Std Dev %)",
    yaxis_title="Cumulative Return 2014–2017 (%)",
    template="plotly_white",
    height=430,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# Page 4
fig_p4_a = go.Figure()
for idx, sym in enumerate(focus_tickers):
    sub = focus_df[focus_df["symbol"] == sym]
    fig_p4_a.add_trace(
        go.Bar(
            x=sub["date"],
            y=sub["volume"] / 1e6,
            name=sym,
            marker_color=PALETTE[sym],
            visible=(idx == 0),
            hovertemplate="Date: %{x|%Y-%m-%d}<br>Volume: %{y:.2f}M shares<extra></extra>",
        )
    )

buttons_p4 = []
for idx, sym in enumerate(focus_tickers):
    vis_list = [i == idx for i in range(len(focus_tickers))]
    buttons_p4.append(
        dict(
            label=sym,
            method="update",
            args=[
                {"visible": vis_list},
                {"title": f"Daily Trading Volume Trend (Millions): {sym}"},
            ],
        )
    )

fig_p4_a.update_layout(
    title=dict(text="Daily Trading Volume Trend (Millions): NVDA", font=dict(size=15)),
    yaxis_title="Volume (Millions of Shares)",
    template="plotly_white",
    height=430,
    xaxis_rangeslider_visible=True,
    xaxis_rangeslider_thickness=0.07,
    updatemenus=[
        dict(
            active=0,
            buttons=buttons_p4,
            x=0.0,
            y=1.16,
            xanchor="left",
            yanchor="top",
            bgcolor="#F1F5F9",
            bordercolor="#CBD5E1",
        )
    ],
)

fig_p4_b = go.Figure()
for sym in focus_tickers:
    sub = focus_df[focus_df["symbol"] == sym].dropna(subset=["daily_return_pct"])
    fig_p4_b.add_trace(
        go.Scatter(
            x=sub["volume"] / 1e6,
            y=sub["daily_return_pct"].abs(),
            mode="markers",
            name=sym,
            marker=dict(color=PALETTE[sym], opacity=0.55, size=6),
            hovertemplate=f"<b>{sym}</b><br>Volume: %{{x:.2f}}M<br>|Daily Return|: %{{y:.2f}}%<extra></extra>",
        )
    )
fig_p4_b.update_layout(
    title=dict(text="Volume vs. Magnitude of Daily Move (|Daily Return %|)", font=dict(size=15)),
    xaxis_title="Daily Volume (Millions of Shares)",
    yaxis_title="Absolute Daily Return (%)",
    template="plotly_white",
    height=430,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

table_rows = ""
for _, r in focus_summary.iterrows():
    ret_color = "#065F46" if r["total_return_pct"] >= 0 else "#DC2626"
    table_rows += f"""
    <tr>
        <td><b>{r['symbol']}</b></td>
        <td>${r['start_close']:.2f}</td>
        <td>${r['end_close']:.2f}</td>
        <td>${r['min_close']:.2f} – ${r['max_close']:.2f}</td>
        <td style="color:{ret_color}; font-weight:bold;">{r['total_return_pct']:+.2f}%</td>
        <td>{r['avg_daily_return_pct']:+.3f}%</td>
        <td>{r['volatility_pct']:.2f}%</td>
        <td>{r['avg_daily_volume']/1e6:.2f}M</td>
        <td>{r['max_daily_volume']/1e6:.2f}M</td>
    </tr>
    """

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>S&P 500 Market Intelligence Dashboard (2014–2017)</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #F1F5F9; color: #0F172A; }}
        header {{ background: #064E3B; color: white; padding: 18px 32px; display: flex; justify-content: space-between; align-items: center; }}
        header h1 {{ margin: 0; font-size: 21px; }}
        header span {{ font-size: 13px; color: #93C5FD; font-weight: 600; }}
        .nav-tabs {{ background: #0F172A; padding: 0 32px; display: flex; gap: 8px; }}
        .tab-btn {{ background: transparent; color: #CBD5E1; border: none; padding: 14px 20px; font-size: 14px; font-weight: 600; cursor: pointer; border-bottom: 3px solid transparent; }}
        .tab-btn.active {{ color: #FFFFFF; border-bottom: 3px solid #2563EB; background: rgba(255,255,255,0.08); }}
        .container {{ max-width: 1320px; margin: 24px auto; padding: 0 24px; }}
        .page {{ display: none; }}
        .page.active {{ display: block; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 22px; }}
        .kpi-card {{ background: white; padding: 18px 20px; border-radius: 8px; border-left: 4px solid #065F46; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .kpi-card.accent {{ border-left-color: #2563EB; }}
        .kpi-title {{ font-size: 12px; text-transform: uppercase; color: #64748B; font-weight: 700; }}
        .kpi-value {{ font-size: 24px; font-weight: 700; margin-top: 6px; color: #064E3B; }}
        .kpi-sub {{ font-size: 12px; color: #475569; margin-top: 4px; }}
        .chart-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
        .card {{ background: white; padding: 18px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
        th {{ background: #064E3B; color: white; text-align: left; padding: 10px 12px; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #E2E8F0; }}
        tr:hover {{ background: #F8FAFC; }}
        .note {{ font-size: 12.5px; color: #475569; margin-top: 8px; }}
    </style>
</head>
<body>
    <header>
        <div>
            <h1>S&P 500 Stock Market Intelligence Dashboard (2014–2017)</h1>
            <div style="font-size:12px; color:#D1FAE5; margin-top:3px;">Historical Market Performance, Returns, Volatility & Volume Analytics | OGD Analytics</div>
        </div>
        <span>AnalystLab Africa • Week 6 Track A</span>
    </header>
    <div class="nav-tabs">
        <button class="tab-btn active" onclick="openPage('page1', this)">Page 1: Market Overview</button>
        <button class="tab-btn" onclick="openPage('page2', this)">Page 2: Stock Price Performance</button>
        <button class="tab-btn" onclick="openPage('page3', this)">Page 3: Returns & Volatility</button>
        <button class="tab-btn" onclick="openPage('page4', this)">Page 4: Trading Volume Analysis</button>
    </div>

    <div class="container">
        <div id="page1" class="page active">
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Total Stock Symbols</div>
                    <div class="kpi-value">505</div>
                    <div class="kpi-sub">479 with full 1,007-day history</div>
                </div>
                <div class="kpi-card accent">
                    <div class="kpi-title">Total Trading Records</div>
                    <div class="kpi-value">497,472</div>
                    <div class="kpi-sub">Jan 2, 2014 – Dec 29, 2017</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Market Mean Closing Price</div>
                    <div class="kpi-value">$86.37</div>
                    <div class="kpi-sub">Median: $64.98 | Peak: $2,049.00 (PCLN)</div>
                </div>
                <div class="kpi-card accent">
                    <div class="kpi-title">Top Cumulative Gainer</div>
                    <div class="kpi-value">NVDA (+1,120.1%)</div>
                    <div class="kpi-sub">$15.86 → $193.50 (2014–2017)</div>
                </div>
            </div>
            <div class="chart-grid-2">
                <div class="card"><div id="chart_p1_a"></div></div>
                <div class="card"><div id="chart_p1_b"></div></div>
            </div>
            <div class="card">
                <h3 style="margin-top:0; color:#064E3B;">Comparative Performance Summary: 6 Focus Stocks (Full 1,007 Trading Days)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Symbol</th><th>Start Close</th><th>End Close</th><th>Min–Max Range</th>
                            <th>Cumulative Return</th><th>Avg Daily Return</th><th>Daily Volatility</th>
                            <th>Avg Daily Vol</th><th>Peak Daily Vol</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows}</tbody>
                </table>
                <div class="note">Note: Historical data covers 2014–2017 and does not represent current market prices or future investment guarantees.</div>
            </div>
        </div>

        <div id="page2" class="page">
            <div class="card">
                <div id="chart_p2"></div>
                <div class="note">Tip: Use the dropdown button above the chart to switch between NVDA, AMZN, AAPL, BAC, JNJ, and CHK, and drag the bottom range slider to filter dates.</div>
            </div>
        </div>

        <div id="page3" class="page">
            <div class="chart-grid-2">
                <div class="card"><div id="chart_p3_a"></div></div>
                <div class="card"><div id="chart_p3_b"></div></div>
            </div>
            <div class="card">
                <h3 style="margin-top:0; color:#064E3B;">Key Statistical Takeaways on Return vs. Risk</h3>
                <ul style="line-height:1.7; margin-bottom:0;">
                    <li><b>High-Return Efficiency (NVDA):</b> Delivered +1,120.05% cumulative return with 2.37% daily volatility—roughly half the volatility of CHK (4.55%).</li>
                    <li><b>Defensive Stability (JNJ):</b> Recorded the lowest daily volatility among focus stocks (0.89%) while compounding a +53.49% gain.</li>
                    <li><b>Uncompensated Volatility (CHK):</b> Highest daily return swings (4.55% std dev) resulted in an -85.12% cumulative drawdown, proving high volatility does not guarantee positive returns.</li>
                </ul>
            </div>
        </div>

        <div id="page4" class="page">
            <div class="chart-grid-2">
                <div class="card"><div id="chart_p4_a"></div></div>
                <div class="card"><div id="chart_p4_b"></div></div>
            </div>
            <div class="card">
                <h3 style="margin-top:0; color:#064E3B;">Trading Volume & Price Movement Insights</h3>
                <ul style="line-height:1.7; margin-bottom:0;">
                    <li><b>Liquidity Leaders:</b> Bank of America (BAC) led the entire S&P 500 with 89.99B total shares traded (89.36M daily avg), followed by Apple (AAPL) at 45.49B shares (45.17M daily avg).</li>
                    <li><b>Volume Correlates with Move Magnitude, Not Direction:</b> Across all 6 focus stocks, correlation between volume and signed daily return is near zero (-0.07 to +0.14), whereas correlation between volume and <b>absolute</b> return size is strong (+0.49 to +0.74)—spikes in volume accompany big news events regardless of direction.</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        const figP1A = {fig_p1_a.to_json()};
        const figP1B = {fig_p1_b.to_json()};
        const figP2  = {fig_p2.to_json()};
        const figP3A = {fig_p3_a.to_json()};
        const figP3B = {fig_p3_b.to_json()};
        const figP4A = {fig_p4_a.to_json()};
        const figP4B = {fig_p4_b.to_json()};

        Plotly.newPlot('chart_p1_a', figP1A.data, figP1A.layout, {{responsive: true}});
        Plotly.newPlot('chart_p1_b', figP1B.data, figP1B.layout, {{responsive: true}});
        Plotly.newPlot('chart_p2',  figP2.data,  figP2.layout,  {{responsive: true}});
        Plotly.newPlot('chart_p3_a', figP3A.data, figP3A.layout, {{responsive: true}});
        Plotly.newPlot('chart_p3_b', figP3B.data, figP3B.layout, {{responsive: true}});
        Plotly.newPlot('chart_p4_a', figP4A.data, figP4A.layout, {{responsive: true}});
        Plotly.newPlot('chart_p4_b', figP4B.data, figP4B.layout, {{responsive: true}});

        function openPage(pageId, btn) {{
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(pageId).classList.add('active');
            btn.classList.add('active');
            window.dispatchEvent(new Event('resize'));
        }}
    </script>
</body>
</html>
"""

out_html = "visuals/SP500_Interactive_Dashboard.html"
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"SUCCESS! Updated Dashboard saved to '{out_html}' with Emerald & Cobalt theme.")