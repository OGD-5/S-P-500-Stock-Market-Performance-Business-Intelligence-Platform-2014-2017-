# 📈 S&P 500 Stock Market Performance & Business Intelligence Platform (2014–2017)

**Author:** Olabode Goodness Daniel (OGD Analytics)  
**Programme:** AnalystLab Africa Experience Lab Internship Programme  
**Week:** 6 | **Track:** A, Data Analytics

---

## 📌 Project Overview

This project explores historical stock market performance across 505 S&P 500 companies using 497,472 daily stock records covering January 2, 2014, to December 29, 2017.

The goal was to build an end-to-end financial market analytics pipeline that transforms raw stock price data into meaningful performance indicators, comparative analysis, and interactive business intelligence dashboards.

Using Python, I carried out data inspection, cleaning, feature engineering, statistical analysis, and visualisation, culminating in a four-page interactive Plotly dashboard.

## 🎯 Business Problem

Financial analysts cannot make meaningful comparisons between stocks by looking at nominal share prices alone. A stock with a high share price does not necessarily deliver the highest percentage return, while high volatility does not automatically indicate strong performance.

This project addresses the need for a structured approach to historical equity analysis by investigating:

- How stock prices and percentage returns changed over the observation period.
- Which stocks delivered the strongest and weakest cumulative returns.
- How historical volatility differs across companies.
- How trading volume relates to daily price movements.
- How selected stocks compare in terms of performance, risk, and liquidity.
- How data quality affects reliable market comparisons.

## 🛠️ Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Jupyter Notebook

## 📊 Dashboard Preview

The project includes a four-page interactive Plotly dashboard designed to make historical market performance easier to explore.

### Dashboard Screenshots

**Page 1: Market Overview**

![S&P 500 Dashboard Page 1](visuals/dashboard_page_1.png)

**Page 2: Stock Performance Analysis**

![S&P 500 Dashboard Page 2](visuals/dashboard_page_2.png)

**Page 3: Risk and Volatility Analysis**

![S&P 500 Dashboard Page 3](visuals/dashboard_page_3.png)

**Page 4: Comparative Stock Analysis**

![S&P 500 Dashboard Page 4](visuals/dashboard_page_4.png)

*Note: Replace the illustrative image paths above with the exact screenshot filenames saved in the `visuals/` folder.*

### Interactive Dashboard

The complete dashboard is available as an HTML file.

[Explore the Interactive S&P 500 Dashboard](visuals/SP500_Interactive_Dashboard.html)

## 🔍 Key Areas of Analysis

### 1. Historical Stock Performance
- Analysed historical closing prices across the S&P 500 symbols.
- Examined daily and cumulative percentage returns.
- Identified stocks with outstanding historical performance.

### 2. Risk and Volatility Analysis
- Calculated daily return volatility for individual stocks.
- Examined differences between high-return and high-volatility stocks.
- Compared historical risk and return characteristics.

### 3. Trading Volume and Liquidity
- Examined average daily trading volume.
- Identified stocks with high trading activity.
- Investigated relationships between trading volume and the magnitude of daily price movements.

### 4. Comparative Analysis of Selected Stocks

Six stocks were selected for a more focused comparison:

- NVIDIA (NVDA)
- Amazon (AMZN)
- Apple (AAPL)
- Bank of America (BAC)
- Johnson & Johnson (JNJ)
- Chesapeake Energy (CHK)

The comparison considered cumulative returns, daily volatility, closing price ranges, and average trading volume.

## 📈 Key Business Findings

### 1. Highest Share Price Did Not Mean Highest Percentage Return

Priceline (PCLN) recorded the highest closing price in the dataset at $2,049.00, but its cumulative return was 51.71%.

NVIDIA (NVDA), despite its much lower starting price, recorded a cumulative return of 1,120.05% between 2014 and 2017.

This demonstrates why percentage returns provide a more meaningful basis for comparing stocks with different nominal prices.

### 2. The Market Experienced a Broad Multi-Year Upward Trend

Across the 479 stocks with complete historical records, mean closing prices increased by 29.3% between 2014 and 2017.

The overall upward movement included a relatively flat period in 2015 before stronger performance in 2016 and 2017.

### 3. Higher Volatility Did Not Guarantee Higher Returns

Chesapeake Energy (CHK) recorded the highest daily volatility among the complete-history stocks at 4.55%, alongside the weakest cumulative return of -85.12%.

In contrast, Johnson & Johnson (JNJ) delivered a 53.49% cumulative return with comparatively lower daily volatility of 0.89%.

### 4. Trading Volume Was Concentrated in Major Financial and Technology Stocks

Bank of America (BAC) recorded the highest total trading volume at approximately 89.99 billion shares, followed by Apple (AAPL) at approximately 45.49 billion shares.

This highlights differences in trading activity and liquidity across major companies.

### 5. Trading Volume Was More Closely Related to Price Movement Magnitude Than Direction

Across the six selected stocks, the relationship between trading volume and signed daily returns was generally weak.

However, trading volume showed a stronger positive relationship with the absolute magnitude of daily returns, with correlations ranging from approximately 0.49 to 0.74.

This suggests that increased trading activity was more closely associated with larger price movements than with whether prices moved upward or downward.

## 💡 Business Recommendations

Based on the analysis, the following recommendations were identified:

1. **Prioritise Percentage Returns and Risk Measures:** Equity screening should consider percentage returns alongside historical volatility rather than relying on nominal share prices alone.

2. **Filter for Complete Historical Records:** Multi-year stock comparisons should account for incomplete trading histories to avoid misleading performance and volume rankings.

3. **Use Trading Volume as a Volatility Monitoring Indicator:** Unusual volume increases can help identify periods of heightened market activity and potentially larger price movements, rather than being treated as direct bullish or bearish signals.

## 🧹 Data Cleaning and Quality Assessment

The project included a detailed data quality audit to improve the reliability of the analysis.

Key checks included:

- Missing values in Open, High, and Low price fields.
- Duplicate stock-date records.
- Zero-volume trading records.
- Incomplete stock histories.
- Validation of calculated returns and moving averages.

The audit identified 11 missing Open price values and 8 missing High and Low values. These were imputed using the corresponding session's valid closing price, while quality flags were retained.

Four zero-volume records were also identified and flagged.

Of the 505 stock symbols, 479 had complete histories across all 1,007 trading days. Comparisons requiring full historical coverage were restricted to those 479 symbols.

## ⚙️ Feature Engineering and KPI Development

Additional analytical features were created to support deeper market analysis.

These included:

- Daily Price Change
- Daily Percentage Return
- Cumulative Return
- Historical Volatility
- Daily Trading Range
- 20-Day Moving Average
- 50-Day Moving Average
- Average Daily Trading Volume
- Trading Days Count
- Complete Historical Record Flag

All rolling calculations and return calculations were performed separately for each stock symbol to avoid mixing records from different companies.

## 📂 Repository Structure

```text
S&P-500-Market-Analytics/
│
├── data/
│   ├── raw/
│   │   └── S&P 500 Stock Prices 2014-2017.csv
│   │
│   └── processed/
│       ├── sp500_cleaned.csv
│       ├── stock_kpi_summary.csv
│       └── focus_stocks_comparison.csv
│
├── scripts/
│   ├── 01_data_prep.py
│   ├── 02_market_analysis.py
│   ├── 03_dashboard.py
│   └── 04_build_deliverables.py
│
├── notebooks/
│   └── SP500_Market_Intelligence.ipynb
│
├── visuals/
│   ├── Static PNG Charts
│   ├── Dashboard Screenshots
│   └── SP500_Interactive_Dashboard.html
│
├── docs/
│   ├── KPI_Definition_Sheet.md
│   ├── Data_Quality_and_Validation.md
│   └── Executive_Summary.md
│
└── README.md
```

## ▶️ How to Reproduce the Analysis

### 1. Install the Required Libraries

```bash
pip install pandas numpy matplotlib seaborn plotly jupyter
```

### 2. Run the Python Scripts

From the project root directory, execute the scripts in the following order:

```bash
python scripts/01_data_prep.py
python scripts/02_market_analysis.py
python scripts/03_dashboard.py
python scripts/04_build_deliverables.py
```

### 3. Explore the Dashboard

Open `visuals/SP500_Interactive_Dashboard.html` in a modern web browser to explore all four interactive dashboard pages.

### 4. Explore the Notebook

Open `notebooks/SP500_Market_Intelligence.ipynb` using Jupyter Notebook to review the analytical workflow.

## 📚 Project Documentation

Additional documentation is available in the `docs/` directory:

- **KPI Definition Sheet:** Explains the financial metrics, calculation methods, units, and analytical interpretations.
- **Data Quality and Validation:** Documents identified data quality issues, remediation steps, and independent calculation checks.
- **Executive Summary:** Provides a concise overview of the business problem, key findings, and recommendations.

## ⚠️ Assumptions and Limitations

- **Historical Coverage:** The analysis covers 2014–2017 and does not represent current market prices or future performance.
- **Unadjusted Prices:** The dataset does not contain explicit dividend or stock-split adjustment columns. Cumulative returns therefore reflect raw historical close-to-close price changes.
- **Currency:** All stock prices are denominated in USD.
- **Trading Volume:** Volume represents the number of shares traded, not dollar turnover.
- **Investment Disclaimer:** Historical performance does not guarantee future returns. This project is for educational and analytical purposes, not investment advice.

## 🎓 Learning Outcomes

This project strengthened my practical skills in:

- Python-based financial data analysis.
- Data cleaning and quality validation.
- Feature engineering and rolling calculations.
- Financial KPI development.
- Historical stock performance analysis.
- Risk, return, and liquidity comparisons.
- Interactive dashboard development with Plotly.
- Building reproducible analytical pipelines.
- Communicating analytical findings through business recommendations.

---

**Project completed as part of the AnalystLab Africa Experience Lab Internship Programme, Week 6, Data Analytics Track.**
