# ============================================================
# NOTEBOOK 2 — Exploratory Data Analysis (EDA)
# Project : E-Commerce Sales & Customer Analytics
# ============================================================

import os
import seaborn as sns
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — saves PNGs

CLEAN = "/Users/shireen/sales dashboard analysis /project/data/superstore_clean.csv"
IMGDIR = "/Users/shireen/sales dashboard analysis /project/images"
os.makedirs(IMGDIR, exist_ok=True)

df = pd.read_csv(CLEAN, parse_dates=["order_date", "ship_date"])

# ── colour palette ────────────────────────────────────────────
PALETTE = ["#2196F3", "#FF5722", "#4CAF50", "#FFC107", "#9C27B0"]
sns.set_theme(style="whitegrid", font_scale=1.1)


def save(name):
    path = os.path.join(IMGDIR, name)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ saved → images/{name}")


# ═══════════════════════════════════════════════════════════════
# ANALYSIS 1 — YEARLY SALES & PROFIT TREND
# Business Question: Is the company growing year over year?
# ═══════════════════════════════════════════════════════════════
yearly = df.groupby("year")[["sales", "profit"]].sum().reset_index()
yearly["profit_margin"] = (yearly["profit"] / yearly["sales"] * 100).round(1)

print("── YEARLY SALES & PROFIT ──")
print(yearly.to_string(index=False))

fig, ax1 = plt.subplots(figsize=(9, 5))
ax2 = ax1.twinx()
ax1.bar(yearly["year"], yearly["sales"],
        color=PALETTE[0], alpha=0.7, label="Sales")
ax1.bar(yearly["year"], yearly["profit"],
        color=PALETTE[2], alpha=0.9, label="Profit")
ax2.plot(yearly["year"], yearly["profit_margin"], color=PALETTE[1],
         marker="o", linewidth=2.5, label="Profit Margin %")
ax1.set_xlabel("Year")
ax1.set_ylabel("USD ($)")
ax2.set_ylabel("Profit Margin (%)")
ax1.set_title("Yearly Sales & Profit Trend", fontsize=14, fontweight="bold")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save("01_yearly_trend.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 2 — SALES BY CATEGORY
# Business Question: Which product category drives revenue?
# ═══════════════════════════════════════════════════════════════
cat = df.groupby("category")[["sales", "profit"]
                             ].sum().sort_values("sales", ascending=False)
print("\n── SALES & PROFIT BY CATEGORY ──")
print(cat)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
cat["sales"].plot(kind="bar",  ax=axes[0], color=PALETTE[0], edgecolor="white")
cat["profit"].plot(kind="bar", ax=axes[1], color=PALETTE[2], edgecolor="white")
axes[0].set_title("Total Sales by Category",  fontweight="bold")
axes[1].set_title("Total Profit by Category", fontweight="bold")
for ax in axes:
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=15)
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
save("02_category_sales_profit.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 3 — SALES BY SUB-CATEGORY
# Business Question: Which sub-categories are most/least profitable?
# ═══════════════════════════════════════════════════════════════
sub = df.groupby("sub_category")[
    ["sales", "profit"]].sum().sort_values("profit")
print("\n── TOP/BOTTOM SUB-CATEGORIES BY PROFIT ──")
print(sub)

fig, ax = plt.subplots(figsize=(12, 7))
colors = [PALETTE[1] if v < 0 else PALETTE[2] for v in sub["profit"]]
sub["profit"].plot(kind="barh", ax=ax, color=colors, edgecolor="white")
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Profit by Sub-Category (Red = Loss)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Total Profit ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save("03_subcategory_profit.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 4 — REGIONAL PERFORMANCE
# Business Question: Which regions are most profitable?
# ═══════════════════════════════════════════════════════════════
region = df.groupby("region")[["sales", "profit"]
                              ].sum().sort_values("sales", ascending=False)
region["margin"] = (region["profit"] / region["sales"] * 100).round(1)
print("\n── REGIONAL PERFORMANCE ──")
print(region)

fig, ax = plt.subplots(figsize=(11, 5))
x = range(len(region))
bars = ax.bar([i - 0.2 for i in x], region["sales"],
              width=0.35, label="Sales",  color=PALETTE[0])
bars = ax.bar([i + 0.2 for i in x], region["profit"],
              width=0.35, label="Profit", color=PALETTE[2])
ax.set_xticks(list(x))
ax.set_xticklabels(region.index, rotation=30, ha="right")
ax.set_title("Sales & Profit by Region", fontsize=14, fontweight="bold")
ax.set_ylabel("USD ($)")
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save("04_regional_performance.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 5 — DISCOUNT vs PROFIT (Scatter)
# Business Question: Are discounts hurting profit margins?
# ═══════════════════════════════════════════════════════════════
sample = df.sample(min(3000, len(df)), random_state=42)

fig, ax = plt.subplots(figsize=(9, 5))
scatter = ax.scatter(sample["discount"], sample["profit"],
                     c=sample["profit"], cmap="RdYlGn",
                     alpha=0.5, s=18, edgecolors="none")
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.axvline(0.2, color=PALETTE[1], linewidth=1.2,
           linestyle="--", label="20% Discount line")
plt.colorbar(scatter, ax=ax, label="Profit")
ax.set_xlabel("Discount Rate")
ax.set_ylabel("Profit ($)")
ax.set_title("Discount Rate vs Profit per Order",
             fontsize=14, fontweight="bold")
ax.legend()
save("05_discount_vs_profit.png")

# Discount bracket summary
disc = df.groupby("discount_bracket", observed=True)[
    ["sales", "profit", "quantity"]].mean().round(2)
disc["avg_margin"] = (disc["profit"] / disc["sales"] * 100).round(1)
print("\n── AVERAGE METRICS BY DISCOUNT BRACKET ──")
print(disc)

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 6 — SEGMENT ANALYSIS
# Business Question: Which customer segment is most valuable?
# ═══════════════════════════════════════════════════════════════
seg = df.groupby("segment")[["sales", "profit"]].sum()
seg["margin"] = (seg["profit"] / seg["sales"] * 100).round(1)
print("\n── SEGMENT PERFORMANCE ──")
print(seg)

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
axes[0].pie(seg["sales"], labels=seg.index, autopct="%1.1f%%",
            colors=PALETTE[:3], startangle=140)
axes[0].set_title("Sales Share by Segment", fontweight="bold")
axes[1].pie(seg["profit"], labels=seg.index, autopct="%1.1f%%",
            colors=PALETTE[:3], startangle=140)
axes[1].set_title("Profit Share by Segment", fontweight="bold")
plt.tight_layout()
save("06_segment_analysis.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 7 — TOP 10 CUSTOMERS BY REVENUE
# Business Question: Who are our most valuable customers?
# ═══════════════════════════════════════════════════════════════
top_cust = (df.groupby("customer_name")[["sales", "profit"]]
              .sum()
              .sort_values("sales", ascending=False)
              .head(10))
print("\n── TOP 10 CUSTOMERS BY REVENUE ──")
print(top_cust)

fig, ax = plt.subplots(figsize=(11, 6))
top_cust["sales"].sort_values().plot(
    kind="barh", ax=ax, color=PALETTE[0], edgecolor="white")
ax.set_title("Top 10 Customers by Total Revenue",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Total Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save("07_top10_customers.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 8 — SHIP MODE PERFORMANCE
# Business Question: Are we spending appropriately on shipping?
# ═══════════════════════════════════════════════════════════════
ship = df.groupby("ship_mode").agg(
    orders=("order_id",     "count"),
    avg_ship_days=("shipping_days", "mean"),
    total_cost=("shipping_cost", "sum"),
    total_profit=("profit",       "sum")
).round(2).sort_values("orders", ascending=False)
print("\n── SHIPPING MODE ANALYSIS ──")
print(ship)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ship["orders"].plot(kind="bar", ax=axes[0],
                    color=PALETTE[3], edgecolor="white")
axes[0].set_title("Order Count by Ship Mode", fontweight="bold")
axes[0].tick_params(axis="x", rotation=20)

ship["avg_ship_days"].plot(kind="bar", ax=axes[1],
                           color=PALETTE[4], edgecolor="white")
axes[1].set_title("Avg Shipping Days by Mode", fontweight="bold")
axes[1].tick_params(axis="x", rotation=20)
plt.tight_layout()
save("08_shipping_analysis.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 9 — MONTHLY SALES TREND (most recent year)
# Business Question: Is there seasonality in our sales?
# ═══════════════════════════════════════════════════════════════
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b")

monthly = (df.groupby(["year", "month", "month_name"])["sales"]
             .sum()
             .reset_index()
             .sort_values(["year", "month"]))

# pivot for multi-year line chart
pivot = monthly.pivot(index="month", columns="year", values="sales")

fig, ax = plt.subplots(figsize=(12, 5))
for col in pivot.columns:
    ax.plot(pivot.index, pivot[col], marker="o", linewidth=2, label=str(col))
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_title("Monthly Sales Trend by Year", fontsize=14, fontweight="bold")
ax.set_ylabel("Total Sales ($)")
ax.legend(title="Year")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save("09_monthly_trend.png")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 10 — MARKET PERFORMANCE
# Business Question: Which global market is most profitable?
# ═══════════════════════════════════════════════════════════════
mkt = df.groupby("market")[["sales", "profit", "shipping_cost"]].sum(
).sort_values("profit", ascending=False)
mkt["margin"] = (mkt["profit"] / mkt["sales"] * 100).round(1)
print("\n── MARKET PERFORMANCE ──")
print(mkt)

fig, ax = plt.subplots(figsize=(11, 5))
x = range(len(mkt))
ax.bar([i - 0.2 for i in x], mkt["sales"],
       width=0.35, label="Sales",  color=PALETTE[0])
ax.bar([i + 0.2 for i in x], mkt["profit"],
       width=0.35, label="Profit", color=PALETTE[2])
ax.set_xticks(list(x))
ax.set_xticklabels(mkt.index, rotation=30, ha="right")
ax.set_title("Sales & Profit by Market", fontsize=14, fontweight="bold")
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save("10_market_performance.png")

print("\n" + "=" * 60)
print("ALL 10 EDA CHARTS SAVED TO /images/")
print("=" * 60)
