# Power BI Dashboard Setup Guide
## E-Commerce Sales & Customer Analytics

---

## Step 1 — Connect to Data

1. Open Power BI Desktop
2. Click **Get Data → Text/CSV**
3. Browse to `data/superstore_clean.csv`
4. Click **Transform Data** to open Power Query Editor
5. Verify column types:
   - `order_date`, `ship_date` → Date
   - `sales`, `profit`, `discount`, `shipping_cost` → Decimal Number
   - `quantity`, `year`, `shipping_days` → Whole Number
   - All others → Text
6. Click **Close & Apply**

---

## Step 2 — Create DAX Measures

In the **Data** view, create a Measures table, then add:

```dax
-- Total Revenue
Total Sales = SUM(orders[sales])

-- Total Profit
Total Profit = SUM(orders[profit])

-- Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0) * 100

-- Total Orders
Total Orders = DISTINCTCOUNT(orders[order_id])

-- Unique Customers
Unique Customers = DISTINCTCOUNT(orders[customer_id])

-- Average Order Value
Avg Order Value = DIVIDE([Total Sales], [Total Orders], 0)

-- Average Shipping Days
Avg Shipping Days = AVERAGE(orders[shipping_days])

-- YoY Sales Growth %
YoY Sales Growth % =
VAR CurrentYear = MAX(orders[year])
VAR CurrentSales = CALCULATE([Total Sales], orders[year] = CurrentYear)
VAR PrevSales    = CALCULATE([Total Sales], orders[year] = CurrentYear - 1)
RETURN
    IF(PrevSales = 0, BLANK(), DIVIDE(CurrentSales - PrevSales, PrevSales) * 100)
```

---

## Step 3 — Dashboard Pages

### Page 1 — Executive Overview
**Visuals:**
- 4 KPI Cards: Total Sales | Total Profit | Profit Margin % | Total Orders
- Line Chart: Sales & Profit by Year
- Bar Chart: Sales by Category
- Donut Chart: Sales by Segment
- Slicer: Year

### Page 2 — Product Analysis
**Visuals:**
- Bar Chart: Top 10 Products by Sales
- Horizontal Bar Chart: Profit by Sub-Category (conditional formatting: red for negative)
- Scatter Plot: Discount vs Profit
- Table: Sub-Category | Sales | Profit | Margin % | Avg Discount
- Slicer: Category | Year

### Page 3 — Regional & Market Analysis
**Visuals:**
- Map Visual: Sales by Country (bubble map)
- Bar Chart: Sales & Profit by Region
- Bar Chart: Sales & Profit by Market
- KPI Card: Best Performing Region
- Slicer: Year | Category

### Page 4 — Customer Analysis
**Visuals:**
- Table: Top 20 Customers by Lifetime Value
- Bar Chart: Sales by Customer Segment
- Column Chart: Order Count by Segment
- KPI Card: Unique Customers | Avg Order Value
- Slicer: Segment | Year

### Page 5 — Shipping & Operations
**Visuals:**
- Bar Chart: Orders by Ship Mode
- Bar Chart: Avg Shipping Days by Ship Mode
- Line Chart: Shipping Cost Trend by Year
- KPI Card: Avg Shipping Days
- Slicer: Ship Mode | Year

---

## Step 4 — Formatting Best Practices

- Company primary colour: `#2196F3` (blue)
- Profit positive colour: `#4CAF50` (green)
- Profit negative colour: `#FF5722` (red/orange)
- Background: White (`#FFFFFF`) or Light Grey (`#F5F5F5`)
- Font: Segoe UI, 11–14pt for labels, 24–32pt for KPI values
- Add a header bar on every page with the page title
- Add a navigation panel on the left with page buttons

---

## Step 5 — Conditional Formatting

For any Profit column in tables or bar charts:
- Go to Format → Conditional Formatting → Background Color
- Rules:
  - If value < 0 → Red (`#FFCDD2`)
  - If value >= 0 → Green (`#C8E6C9`)

---

## Step 6 — Publish

1. Save the `.pbix` file in the `dashboard/` folder
2. Click **Publish** → Select your Power BI workspace
3. Share the link with stakeholders

---

*Follow this guide page by page. Each visual corresponds to a SQL query or Python analysis already built in this project.*
