# ============================================================
# E-Commerce Sales & Customer Analytics Dashboard
# Tool    : Streamlit + Plotly
# Data    : Global Superstore Dataset (2011-2014)
# Run     : streamlit run dashboard/app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    h1 { color: #1a237e; }
    h2 { color: #283593; }
    h3 { color: #3949ab; }
    .sidebar .sidebar-content { background-color: #e8eaf6; }
    </style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────


@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "data", "superstore_clean.csv")
    df = pd.read_csv(path, parse_dates=["order_date", "ship_date"])
    return df


df = load_data()

# ── COLOUR PALETTE ────────────────────────────────────────────
BLUE = "#2196F3"
GREEN = "#4CAF50"
RED = "#F44336"
ORANGE = "#FF9800"
PURPLE = "#9C27B0"
TEAL = "#009688"

# ═══════════════════════════════════════════════════════════════
# SIDEBAR — FILTERS
# ═══════════════════════════════════════════════════════════════
st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart--v1.png", width=80)
st.sidebar.title("🔎 Filters")
st.sidebar.markdown("---")

years = sorted(df["year"].unique().tolist())
selected_years = st.sidebar.multiselect(
    "📅 Select Year(s)",
    options=years,
    default=years
)

categories = sorted(df["category"].unique().tolist())
selected_cats = st.sidebar.multiselect(
    "📦 Select Category",
    options=categories,
    default=categories
)

segments = sorted(df["segment"].unique().tolist())
selected_segs = st.sidebar.multiselect(
    "👥 Select Segment",
    options=segments,
    default=segments
)

regions = sorted(df["region"].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "🌍 Select Region",
    options=regions,
    default=regions
)

st.sidebar.markdown("---")
st.sidebar.markdown("**E-Commerce Analytics Dashboard**")
st.sidebar.markdown("Built with Python · Streamlit · Plotly")
st.sidebar.markdown("Dataset: Global Superstore 2011–2014")

# ── APPLY FILTERS ─────────────────────────────────────────────
filtered = df[
    (df["year"].isin(selected_years)) &
    (df["category"].isin(selected_cats)) &
    (df["segment"].isin(selected_segs)) &
    (df["region"].isin(selected_regions))
]

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("# 📊 E-Commerce Sales & Customer Analytics Dashboard")
st.markdown("**GlobalMart · Global Superstore Dataset · 2011–2014**")
st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# PAGE TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Executive Overview",
    "📦 Product Analysis",
    "🌍 Regional & Market",
    "👥 Customer Analysis",
    "🚚 Shipping & Operations"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE OVERVIEW
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## 🏠 Executive Overview")
    st.markdown("High-level KPIs and business performance at a glance.")
    st.markdown("---")

    # ── KPI CARDS ─────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)

    total_sales = filtered["sales"].sum()
    total_profit = filtered["profit"].sum()
    profit_margin = (total_profit / total_sales *
                     100) if total_sales > 0 else 0
    total_orders = filtered["order_id"].nunique()
    total_customers = filtered["customer_id"].nunique()

    col1.metric("💰 Total Sales",    f"${total_sales:,.0f}")
    col2.metric("📈 Total Profit",   f"${total_profit:,.0f}")
    col3.metric("📊 Profit Margin",  f"{profit_margin:.1f}%")
    col4.metric("🛒 Total Orders",   f"{total_orders:,}")
    col5.metric("👤 Unique Customers", f"{total_customers:,}")

    st.markdown("---")

    # ── YEARLY TREND ──────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📅 Yearly Sales & Profit Trend")
        yearly = filtered.groupby(
            "year")[["sales", "profit"]].sum().reset_index()
        yearly["margin"] = (yearly["profit"] / yearly["sales"] * 100).round(1)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=yearly["year"], y=yearly["sales"],
            name="Sales", marker_color=BLUE, opacity=0.8
        ), secondary_y=False)
        fig.add_trace(go.Bar(
            x=yearly["year"], y=yearly["profit"],
            name="Profit", marker_color=GREEN, opacity=0.9
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=yearly["year"], y=yearly["margin"],
            name="Margin %", line=dict(color=ORANGE, width=3),
            marker=dict(size=8)
        ), secondary_y=True)
        fig.update_layout(
            height=380, plot_bgcolor="white",
            paper_bgcolor="white", barmode="group",
            legend=dict(orientation="h", y=1.12)
        )
        fig.update_yaxes(title_text="USD ($)", secondary_y=False)
        fig.update_yaxes(title_text="Margin (%)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### 🗓️ Monthly Sales Seasonality")
        filtered["month"] = filtered["order_date"].dt.month
        monthly = filtered.groupby(["year", "month"])[
            "sales"].sum().reset_index()
        pivot = monthly.pivot(index="month", columns="year",
                              values="sales").reset_index()

        fig2 = go.Figure()
        colors_line = [BLUE, GREEN, ORANGE, PURPLE]
        for i, yr in enumerate([c for c in pivot.columns if c != "month"]):
            fig2.add_trace(go.Scatter(
                x=pivot["month"], y=pivot[yr],
                name=str(yr), mode="lines+markers",
                line=dict(width=2.5, color=colors_line[i % 4]),
                marker=dict(size=6)
            ))
        fig2.update_layout(
            height=380, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(tickmode="array",
                       tickvals=list(range(1, 13)),
                       ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
            legend=dict(orientation="h", y=1.12),
            yaxis_title="Sales ($)"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── QUARTERLY BREAKDOWN ───────────────────────────────────
    st.markdown("### 📊 Quarterly Sales Breakdown")
    filtered["quarter"] = filtered["order_date"].dt.quarter
    quarterly = filtered.groupby(["year", "quarter"])[
        ["sales", "profit"]].sum().reset_index()
    quarterly["label"] = "Q" + \
        quarterly["quarter"].astype(str) + " " + quarterly["year"].astype(str)

    fig3 = px.bar(
        quarterly, x="label", y="sales",
        color="profit", color_continuous_scale=["red", "yellow", "green"],
        title="Quarterly Sales (colour = profit level)",
        labels={"sales": "Sales ($)", "label": "Quarter"}
    )
    fig3.update_layout(height=350, plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2 — PRODUCT ANALYSIS
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## 📦 Product Analysis")
    st.markdown(
        "Which categories, sub-categories, and products drive revenue and profit?")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Category Sales vs Profit")
        cat = filtered.groupby("category")[
            ["sales", "profit"]].sum().reset_index()
        cat["margin"] = (cat["profit"] / cat["sales"] * 100).round(1)

        fig = px.bar(
            cat, x="category", y=["sales", "profit"],
            barmode="group", color_discrete_sequence=[BLUE, GREEN],
            labels={"value": "USD ($)", "variable": "Metric"}
        )
        fig.update_layout(height=370, plot_bgcolor="white",
                          paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Category Profit Margin %")
        fig2 = px.pie(
            cat, values="profit", names="category",
            color_discrete_sequence=[BLUE, GREEN, ORANGE],
            hole=0.45
        )
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        fig2.update_layout(height=370, paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### Sub-Category Profit (Red = Loss, Green = Profit)")

    sub = filtered.groupby("sub_category")[
        ["sales", "profit"]].sum().reset_index()
    sub["margin"] = (sub["profit"] / sub["sales"] * 100).round(1)
    sub = sub.sort_values("profit")
    sub["color"] = sub["profit"].apply(lambda x: RED if x < 0 else GREEN)

    fig3 = go.Figure(go.Bar(
        x=sub["profit"], y=sub["sub_category"],
        orientation="h",
        marker_color=sub["color"],
        text=sub["profit"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside"
    ))
    fig3.add_vline(x=0, line_color="black", line_width=1)
    fig3.update_layout(
        height=550, plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="Total Profit ($)", yaxis_title=""
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🔴 Discount vs Profit Margin")
        disc = filtered.groupby("discount_bracket", observed=True).agg(
            avg_margin=("profit_margin_pct", "mean"),
            order_count=("order_id", "count")
        ).reset_index()

        fig4 = px.bar(
            disc, x="discount_bracket", y="avg_margin",
            color="avg_margin",
            color_continuous_scale=["red", "yellow", "green"],
            text=disc["avg_margin"].apply(lambda x: f"{x:.1f}%"),
            labels={
                "avg_margin": "Avg Profit Margin (%)", "discount_bracket": "Discount Bracket"}
        )
        fig4.add_hline(y=0, line_color="black", line_dash="dash")
        fig4.update_layout(height=370, plot_bgcolor="white",
                           paper_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        st.markdown("### 📋 Sub-Category Summary Table")
        sub_table = filtered.groupby("sub_category").agg(
            Total_Sales=("sales", "sum"),
            Total_Profit=("profit", "sum"),
            Avg_Discount=("discount", "mean"),
            Orders=("order_id", "count")
        ).reset_index()
        sub_table["Margin_%"] = (
            sub_table["Total_Profit"] / sub_table["Total_Sales"] * 100).round(1)
        sub_table["Total_Sales"] = sub_table["Total_Sales"].apply(
            lambda x: f"${x:,.0f}")
        sub_table["Total_Profit"] = sub_table["Total_Profit"].apply(
            lambda x: f"${x:,.0f}")
        sub_table["Avg_Discount"] = sub_table["Avg_Discount"].apply(
            lambda x: f"{x*100:.1f}%")
        sub_table = sub_table.sort_values("Margin_%", ascending=False)
        st.dataframe(sub_table, use_container_width=True, height=370)


# ═══════════════════════════════════════════════════════════════
# TAB 3 — REGIONAL & MARKET
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## 🌍 Regional & Market Performance")
    st.markdown("Where are we strong and where do we need to improve?")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Regional Sales & Profit")
        region = filtered.groupby(
            "region")[["sales", "profit"]].sum().reset_index()
        region["margin"] = (region["profit"] / region["sales"] * 100).round(1)
        region = region.sort_values("sales", ascending=False)

        fig = px.bar(
            region, x="region", y=["sales", "profit"],
            barmode="group", color_discrete_sequence=[BLUE, GREEN],
            labels={"value": "USD ($)", "variable": "Metric"}
        )
        fig.update_layout(
            height=380, plot_bgcolor="white", paper_bgcolor="white",
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Profit Margin % by Region")
        fig2 = px.bar(
            region.sort_values("margin"),
            x="margin", y="region",
            orientation="h",
            color="margin",
            color_continuous_scale=["red", "yellow", "green"],
            text=region.sort_values("margin")["margin"].apply(
                lambda x: f"{x:.1f}%"),
            labels={"margin": "Profit Margin (%)", "region": ""}
        )
        fig2.add_vline(x=0, line_color="black", line_width=1)
        fig2.update_layout(height=380, plot_bgcolor="white",
                           paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Global Market Performance")
        market = filtered.groupby(
            "market")[["sales", "profit"]].sum().reset_index()
        market["margin"] = (market["profit"] / market["sales"] * 100).round(1)
        market = market.sort_values("profit", ascending=False)

        fig3 = px.bar(
            market, x="market", y=["sales", "profit"],
            barmode="group", color_discrete_sequence=[BLUE, GREEN],
            labels={"value": "USD ($)", "variable": "Metric"}
        )
        fig3.update_layout(
            height=380, plot_bgcolor="white", paper_bgcolor="white",
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("### Market Summary Table")
        mkt_table = filtered.groupby("market").agg(
            Sales=("sales", "sum"),
            Profit=("profit", "sum"),
            Orders=("order_id", "nunique"),
            Customers=("customer_id", "nunique")
        ).reset_index()
        mkt_table["Margin_%"] = (
            mkt_table["Profit"] / mkt_table["Sales"] * 100).round(1)
        mkt_table["Sales"] = mkt_table["Sales"].apply(lambda x: f"${x:,.0f}")
        mkt_table["Profit"] = mkt_table["Profit"].apply(lambda x: f"${x:,.0f}")
        mkt_table = mkt_table.sort_values("Margin_%", ascending=False)
        st.dataframe(mkt_table, use_container_width=True, height=380)

    st.markdown("---")
    st.markdown("### Country-Level Bubble Map")
    country = filtered.groupby("country").agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    ).reset_index()
    country["margin"] = (country["profit"] / country["sales"] * 100).round(1)

    fig4 = px.scatter_geo(
        country, locations="country", locationmode="country names",
        size="sales", color="profit",
        color_continuous_scale=["red", "yellow", "green"],
        hover_name="country",
        hover_data={"sales": ":,.0f", "profit": ":,.0f", "margin": ":.1f"},
        projection="natural earth",
        title="Sales by Country (bubble size = sales, colour = profit)"
    )
    fig4.update_layout(height=480, paper_bgcolor="white")
    st.plotly_chart(fig4, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 4 — CUSTOMER ANALYSIS
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 👥 Customer Analysis")
    st.markdown(
        "Who are our most valuable customers and how are they segmented?")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Sales by Customer Segment")
        seg = filtered.groupby("segment")[
            ["sales", "profit"]].sum().reset_index()
        seg["margin"] = (seg["profit"] / seg["sales"] * 100).round(1)

        fig = px.pie(
            seg, values="sales", names="segment",
            color_discrete_sequence=[BLUE, GREEN, ORANGE],
            hole=0.4,
            title="Revenue Share by Segment"
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(height=370, paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Segment KPIs")
        seg_kpi = filtered.groupby("segment").agg(
            Total_Sales=("sales", "sum"),
            Total_Profit=("profit", "sum"),
            Total_Orders=("order_id", "nunique"),
            Unique_Customers=("customer_id", "nunique")
        ).reset_index()
        seg_kpi["Margin_%"] = (seg_kpi["Total_Profit"] /
                               seg_kpi["Total_Sales"] * 100).round(1)
        seg_kpi["Avg_Order"] = (
            seg_kpi["Total_Sales"] / seg_kpi["Total_Orders"]).round(0)
        seg_kpi["Total_Sales"] = seg_kpi["Total_Sales"].apply(
            lambda x: f"${x:,.0f}")
        seg_kpi["Total_Profit"] = seg_kpi["Total_Profit"].apply(
            lambda x: f"${x:,.0f}")
        seg_kpi["Avg_Order"] = seg_kpi["Avg_Order"].apply(
            lambda x: f"${x:,.0f}")
        st.dataframe(seg_kpi, use_container_width=True, height=220)

        st.markdown("### Orders by Segment & Year")
        seg_yr = filtered.groupby(["year", "segment"])[
            "order_id"].nunique().reset_index()
        fig2 = px.line(
            seg_yr, x="year", y="order_id", color="segment",
            markers=True, color_discrete_sequence=[BLUE, GREEN, ORANGE],
            labels={"order_id": "Number of Orders", "year": "Year"}
        )
        fig2.update_layout(height=250, plot_bgcolor="white",
                           paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🏆 Top 20 Customers by Revenue")

    top_n = st.slider("Select number of top customers to display", 5, 50, 20)
    top_cust = filtered.groupby("customer_name").agg(
        Total_Sales=("sales", "sum"),
        Total_Profit=("profit", "sum"),
        Orders=("order_id", "nunique"),
        Segment=("segment", "first")
    ).reset_index().sort_values("Total_Sales", ascending=False).head(top_n)
    top_cust["Margin_%"] = (top_cust["Total_Profit"] /
                            top_cust["Total_Sales"] * 100).round(1)

    fig3 = px.bar(
        top_cust.sort_values("Total_Sales"),
        x="Total_Sales", y="customer_name",
        orientation="h",
        color="Total_Profit",
        color_continuous_scale=["red", "yellow", "green"],
        text=top_cust.sort_values("Total_Sales")[
            "Total_Sales"].apply(lambda x: f"${x:,.0f}"),
        labels={"Total_Sales": "Total Revenue ($)", "customer_name": ""}
    )
    fig3.update_layout(
        height=max(400, top_n * 22),
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Full Customer Table")
    display = top_cust.copy()
    display["Total_Sales"] = display["Total_Sales"].apply(
        lambda x: f"${x:,.0f}")
    display["Total_Profit"] = display["Total_Profit"].apply(
        lambda x: f"${x:,.0f}")
    st.dataframe(display.reset_index(drop=True), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 5 — SHIPPING & OPERATIONS
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## 🚚 Shipping & Operations")
    st.markdown(
        "How efficient is our fulfillment and what does shipping cost us?")
    st.markdown("---")

    ship = filtered.groupby("ship_mode").agg(
        Orders=("order_id",      "count"),
        Avg_Days=("shipping_days", "mean"),
        Total_Cost=("shipping_cost", "sum"),
        Total_Profit=("profit",        "sum")
    ).reset_index().round(2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Avg Shipping Days",
                f"{filtered['shipping_days'].mean():.1f} days")
    col2.metric("💸 Total Shipping Cost",
                f"${filtered['shipping_cost'].sum():,.0f}")
    col3.metric("🚀 Same Day Orders",
                f"{len(filtered[filtered['ship_mode']=='Same Day']):,}")
    col4.metric("📬 Standard Class",
                f"{len(filtered[filtered['ship_mode']=='Standard Class']):,}")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Order Volume by Ship Mode")
        fig = px.pie(
            ship, values="Orders", names="ship_mode",
            color_discrete_sequence=[BLUE, GREEN, ORANGE, PURPLE],
            hole=0.4
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(height=380, paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("### Avg Shipping Days by Mode")
        fig2 = px.bar(
            ship.sort_values("Avg_Days", ascending=False),
            x="ship_mode", y="Avg_Days",
            color="Avg_Days",
            color_continuous_scale=["green", "yellow", "red"],
            text=ship.sort_values("Avg_Days", ascending=False)[
                "Avg_Days"].apply(lambda x: f"{x:.1f}d"),
            labels={"Avg_Days": "Average Days", "ship_mode": "Ship Mode"}
        )
        fig2.update_layout(height=380, plot_bgcolor="white",
                           paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("### Shipping Cost by Mode")
        fig3 = px.bar(
            ship.sort_values("Total_Cost", ascending=False),
            x="ship_mode", y="Total_Cost",
            color_discrete_sequence=[TEAL],
            text=ship.sort_values("Total_Cost", ascending=False)[
                "Total_Cost"].apply(lambda x: f"${x:,.0f}"),
            labels={"Total_Cost": "Total Cost ($)", "ship_mode": "Ship Mode"}
        )
        fig3.update_layout(height=370, plot_bgcolor="white",
                           paper_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown("### Shipping Days Distribution")
        fig4 = px.histogram(
            filtered, x="shipping_days", color="ship_mode",
            nbins=8, barmode="overlay", opacity=0.7,
            color_discrete_sequence=[BLUE, GREEN, ORANGE, PURPLE],
            labels={"shipping_days": "Days to Ship", "count": "Orders"}
        )
        fig4.update_layout(height=370, plot_bgcolor="white",
                           paper_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("### Shipping Mode Performance Summary")
    ship_display = ship.copy()
    ship_display["Avg_Days"] = ship_display["Avg_Days"].apply(
        lambda x: f"{x:.1f} days")
    ship_display["Total_Cost"] = ship_display["Total_Cost"].apply(
        lambda x: f"${x:,.0f}")
    ship_display["Total_Profit"] = ship_display["Total_Profit"].apply(
        lambda x: f"${x:,.0f}")
    st.dataframe(ship_display, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center>📊 E-Commerce Sales & Customer Analytics Dashboard · "
    "Built with Python, Streamlit & Plotly · "
    "Dataset: Global Superstore 2011–2014</center>",
    unsafe_allow_html=True
)
