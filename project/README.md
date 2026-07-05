# E-Commerce Sales & Customer Analytics Dashboard

A complete end-to-end Data Analytics project built on the Global Superstore dataset.
Covers data cleaning, SQL analysis, Python EDA, visualisation, and business recommendations.

---

## Business Problem

GlobalMart's management needed to understand:
- Why profit margins are inconsistent across regions and categories
- Whether discounts are helping or hurting the business
- Which customers and products drive the most value
- How to prioritise decisions for the next financial year

---

## Dataset

| Property | Value |
|---|---|
| Source | Global Superstore Dataset |
| Rows | 51,290 |
| Columns | 27 (24 after cleaning) |
| Date Range | 2011–2014 |
| Markets | 7 (US, EU, APAC, LATAM, Africa, EMEA, Canada) |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10 | Data cleaning, EDA, visualisation |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib / Seaborn | Charts and graphs |
| MySQL | SQL analysis |
| Power BI | Interactive dashboard |
| Git / GitHub | Version control |

---

## Project Structure

```
project/
│
├── data/
│   ├── superstore.csv           ← Raw data (original)
│   └── superstore_clean.csv     ← Cleaned data (output of notebook 1)
│
├── sql/
│   └── superstore_analysis.sql  ← 25 SQL queries (Basic → Window Functions)
│
├── notebooks/
│   ├── 01_data_cleaning.py      ← Data cleaning & feature engineering
│   └── 02_eda.py                ← 10 EDA analyses with charts
│
├── dashboard/
│   └── superstore_dashboard.pbix ← Power BI dashboard file
│
├── reports/
│   └── business_recommendations.md ← 6 key findings + recommendations
│
├── images/
│   ├── 01_yearly_trend.png
│   ├── 02_category_sales_profit.png
│   ├── 03_subcategory_profit.png
│   ├── 04_regional_performance.png
│   ├── 05_discount_vs_profit.png
│   ├── 06_segment_analysis.png
│   ├── 07_top10_customers.png
│   ├── 08_shipping_analysis.png
│   ├── 09_monthly_trend.png
│   └── 10_market_performance.png
│
├── docs/
│   └── powerbi_setup_guide.md   ← How to build the Power BI dashboard
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run data cleaning
```bash
python3.10 notebooks/01_data_cleaning.py
```

### Step 3 — Run EDA and generate charts
```bash
python3.10 notebooks/02_eda.py
```

### Step 4 — Run SQL analysis
- Open MySQL Workbench
- Create database: `superstore`
- Import `data/superstore_clean.csv` as table `orders`
- Open and run `sql/superstore_analysis.sql`

### Step 5 — Open Power BI Dashboard
- Open `dashboard/superstore_dashboard.pbix`
- Refresh data source pointing to `superstore_clean.csv`

---

## Key Insights

1. **Furniture Tables and Bookcases are being sold at a loss** due to average discounts above 30%.
2. **Technology has the highest profit margin** (~14%) and is the most valuable category.
3. **Central region** has the lowest margin despite solid sales volume.
4. **Top 20% of customers generate approximately 80% of total revenue** — Pareto principle confirmed.
5. **Q4 is peak season** — sales spike 40–60% above Q1/Q2 average.
6. **Premium shipping is overused** for low-value orders, increasing cost without revenue benefit.

---

## Business Recommendations

See full report: [reports/business_recommendations.md](reports/business_recommendations.md)

Summary:
- Cap Furniture discounts at 10%
- Increase Technology marketing
- Introduce VIP loyalty programme for top customers
- Set minimum order value for First Class shipping
- Launch mid-year promotional campaign to reduce Q1/Q2 seasonality dip

---

## Skills Demonstrated

- Data Cleaning & Feature Engineering with Pandas
- SQL from basic SELECT to Window Functions (RANK, DENSE_RANK, Running Totals, Moving Averages)
- Exploratory Data Analysis with business context
- Data Visualisation with Matplotlib and Seaborn
- Business storytelling and stakeholder communication
- Power BI data modelling, DAX measures, and dashboard design
- Professional project documentation

---

## Author

Data Analytics Portfolio Project — Built as part of a structured mentorship program.
