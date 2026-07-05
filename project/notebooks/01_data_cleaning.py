# ============================================================
# NOTEBOOK 1 — Data Cleaning & Dataset Understanding
# Project : E-Commerce Sales & Customer Analytics
# Dataset : Superstore Global Sales Data
# ============================================================

import pandas as pd
import numpy as np
import os

# ── 1. LOAD DATA ──────────────────────────────────────────────
RAW = "/Users/shireen/sales dashboard analysis /project/data/superstore.csv"
df = pd.read_csv(RAW, encoding="latin1")

print("=" * 60)
print("STEP 1 — RAW DATASET OVERVIEW")
print("=" * 60)
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")
print()
print(df.dtypes)

# ── 2. RENAME COLUMNS ─────────────────────────────────────────
# Reason: column names have dots and one Chinese character —
#         clean names make every future query easier to write.
df.rename(columns={
    "Customer.ID": "customer_id",
    "Customer.Name": "customer_name",
    "Order.Date": "order_date",
    "Order.ID": "order_id",
    "Order.Priority": "order_priority",
    "Product.ID": "product_id",
    "Product.Name": "product_name",
    "Ship.Date": "ship_date",
    "Ship.Mode": "ship_mode",
    "Shipping.Cost": "shipping_cost",
    "Sub.Category": "sub_category",
    "Row.ID": "row_id",
    # the Chinese column = "Record Count" — it's always 1, drop later
    list(df.columns)[7]: "record_count",
    "Category": "category",
    "City": "city",
    "Country": "country",
    "Discount": "discount",
    "Market": "market",
    "Profit": "profit",
    "Quantity": "quantity",
    "Region": "region",
    "Sales": "sales",
    "Segment": "segment",
    "State": "state",
    "Year": "year",
    "Market2": "market2",
    "weeknum": "week_num",
}, inplace=True)

print("\n✓ Columns renamed")
print(df.columns.tolist())

# ── 3. PARSE DATES ────────────────────────────────────────────
# Reason: dates stored as strings can't be used for time-series
#         analysis until converted to datetime objects.
df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])

# Derive shipping days — a key operational KPI
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days

print("\n✓ Dates parsed — sample:")
print(df[["order_date", "ship_date", "shipping_days"]].head(3))

# ── 4. DROP USELESS COLUMNS ───────────────────────────────────
# record_count is always 1 — adds no value
# market2 duplicates market — redundant
df.drop(columns=["record_count", "market2", "week_num"], inplace=True)
print("\n✓ Dropped redundant columns")

# ── 5. CHECK MISSING VALUES ───────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5 — MISSING VALUES")
print("=" * 60)
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum()
      > 0 else "No missing values found ✓")

# ── 6. CHECK DUPLICATES ───────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6 — DUPLICATE ROWS")
print("=" * 60)
dupes = df.duplicated().sum()
print(f"Duplicate rows: {dupes}")
if dupes > 0:
    df.drop_duplicates(inplace=True)
    print("✓ Duplicates removed")

# ── 7. DATA TYPE FIXES ────────────────────────────────────────
# Sales column came in as int — convert to float for calculations
df["sales"] = df["sales"].astype(float)

print("\n" + "=" * 60)
print("STEP 7 — FINAL DATA TYPES")
print("=" * 60)
print(df.dtypes)

# ── 8. PROFIT MARGIN COLUMN ───────────────────────────────────
# Feature Engineering: profit margin % per row
# This is one of the most important derived KPIs in retail analytics
df["profit_margin_pct"] = (df["profit"] / df["sales"] * 100).round(2)

# ── 9. DISCOUNT BRACKET ───────────────────────────────────────
# Categorise discount into bands for segmentation analysis
bins = [-0.01, 0.0, 0.1, 0.2, 0.3, 1.01]
labels = ["No Discount", "1-10%", "11-20%", "21-30%", "31%+"]
df["discount_bracket"] = pd.cut(df["discount"], bins=bins, labels=labels)

# ── 10. SAVE CLEAN FILE ───────────────────────────────────────
CLEAN = "/Users/shireen/sales dashboard analysis /project/data/superstore_clean.csv"
df.to_csv(CLEAN, index=False)

print("\n" + "=" * 60)
print("STEP 10 — CLEAN DATASET SAVED")
print("=" * 60)
print(f"Shape  : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Saved  : {CLEAN}")

# ── 11. SUMMARY STATISTICS ────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 11 — SUMMARY STATISTICS (numeric columns)")
print("=" * 60)
print(df[["sales", "profit", "quantity", "discount", "shipping_cost",
      "profit_margin_pct", "shipping_days"]].describe().round(2))
