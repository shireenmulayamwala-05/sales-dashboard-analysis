-- ============================================================
-- FILE     : superstore_analysis.sql
-- PROJECT  : E-Commerce Sales & Customer Analytics
-- DATABASE : MySQL
-- DATASET  : Superstore Global Sales
-- ============================================================
-- HOW TO USE:
-- 1. Create the database in MySQL Workbench
-- 2. Import the clean CSV (superstore_clean.csv) as table 'orders'
-- 3. Run each section one at a time
-- ============================================================


-- ── SETUP ─────────────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS superstore;
USE superstore;

-- ── CREATE TABLE ──────────────────────────────────────────────
-- Each column matches the clean CSV produced by 01_data_cleaning.py
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    row_id           INT,
    order_id         VARCHAR(50),
    order_date       DATE,
    ship_date        DATE,
    ship_mode        VARCHAR(50),
    customer_id      VARCHAR(50),
    customer_name    VARCHAR(100),
    segment          VARCHAR(50),
    country          VARCHAR(100),
    city             VARCHAR(100),
    state            VARCHAR(100),
    region           VARCHAR(50),
    market           VARCHAR(50),
    product_id       VARCHAR(50),
    category         VARCHAR(50),
    sub_category     VARCHAR(50),
    product_name     VARCHAR(255),
    sales            DECIMAL(10,2),
    quantity         INT,
    discount         DECIMAL(5,4),
    profit           DECIMAL(10,4),
    shipping_cost    DECIMAL(10,2),
    order_priority   VARCHAR(20),
    year             INT,
    shipping_days    INT,
    profit_margin_pct DECIMAL(8,2),
    discount_bracket VARCHAR(20)
);

-- After creating the table, import the CSV using MySQL Workbench
-- Table Data Import Wizard → select superstore_clean.csv


-- ============================================================
-- SECTION 1 — BASIC SELECT & FILTERING
-- Concept   : SELECT, WHERE, ORDER BY
-- ============================================================

-- Q1: Show all columns for the first 10 orders
SELECT * FROM orders LIMIT 10;

-- Q2: All orders from the Technology category
SELECT order_id, customer_name, product_name, sales, profit
FROM orders
WHERE category = 'Technology'
ORDER BY sales DESC
LIMIT 20;

-- Q3: Orders with discount greater than 30%
SELECT order_id, product_name, discount, sales, profit
FROM orders
WHERE discount > 0.30
ORDER BY discount DESC;

-- Q4: Orders that resulted in a loss (profit < 0)
SELECT order_id, product_name, category, sub_category,
       sales, profit, discount
FROM orders
WHERE profit < 0
ORDER BY profit ASC
LIMIT 20;


-- ============================================================
-- SECTION 2 — AGGREGATION & GROUP BY
-- Concept   : SUM, COUNT, AVG, GROUP BY
-- ============================================================

-- Q5: Total Sales and Profit by Year
SELECT
    year,
    SUM(sales)                                  AS total_sales,
    SUM(profit)                                 AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2)        AS profit_margin_pct,
    COUNT(DISTINCT order_id)                    AS total_orders
FROM orders
GROUP BY year
ORDER BY year;

-- Q6: Sales and Profit by Category
SELECT
    category,
    SUM(sales)                              AS total_sales,
    SUM(profit)                             AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2)    AS margin_pct,
    COUNT(DISTINCT order_id)               AS order_count
FROM orders
GROUP BY category
ORDER BY total_sales DESC;

-- Q7: Sales and Profit by Sub-Category (sorted by profit)
SELECT
    sub_category,
    SUM(sales)                              AS total_sales,
    SUM(profit)                             AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2)    AS margin_pct
FROM orders
GROUP BY sub_category
ORDER BY total_profit DESC;

-- Q8: Performance by Region
SELECT
    region,
    SUM(sales)                              AS total_sales,
    SUM(profit)                             AS total_profit,
    ROUND(AVG(discount)*100, 2)             AS avg_discount_pct,
    ROUND(SUM(profit)/SUM(sales)*100, 2)    AS margin_pct
FROM orders
GROUP BY region
ORDER BY total_profit DESC;

-- Q9: Performance by Market (global)
SELECT
    market,
    SUM(sales)                              AS total_sales,
    SUM(profit)                             AS total_profit,
    COUNT(DISTINCT customer_id)            AS unique_customers,
    ROUND(SUM(profit)/SUM(sales)*100, 2)    AS margin_pct
FROM orders
GROUP BY market
ORDER BY total_profit DESC;

-- Q10: Average Shipping Days by Ship Mode
SELECT
    ship_mode,
    COUNT(*)                        AS order_count,
    ROUND(AVG(shipping_days), 1)    AS avg_days,
    ROUND(SUM(shipping_cost), 2)    AS total_shipping_cost
FROM orders
GROUP BY ship_mode
ORDER BY avg_days;


-- ============================================================
-- SECTION 3 — HAVING (Filter on Aggregated Results)
-- ============================================================

-- Q11: Sub-categories where average discount > 20%
SELECT
    sub_category,
    ROUND(AVG(discount)*100, 2)     AS avg_discount_pct,
    SUM(profit)                     AS total_profit
FROM orders
GROUP BY sub_category
HAVING avg_discount_pct > 20
ORDER BY avg_discount_pct DESC;

-- Q12: Customers who spent more than $5,000 total
SELECT
    customer_name,
    segment,
    SUM(sales)              AS lifetime_value,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(profit)             AS total_profit_generated
FROM orders
GROUP BY customer_name, segment
HAVING lifetime_value > 5000
ORDER BY lifetime_value DESC;


-- ============================================================
-- SECTION 4 — CASE STATEMENTS
-- ============================================================

-- Q13: Classify each order by profit level
SELECT
    order_id,
    customer_name,
    sales,
    profit,
    CASE
        WHEN profit > 500  THEN 'High Profit'
        WHEN profit > 0    THEN 'Low Profit'
        WHEN profit = 0    THEN 'Break Even'
        ELSE 'Loss'
    END AS profit_class
FROM orders
ORDER BY profit DESC
LIMIT 30;

-- Q14: Discount impact classification
SELECT
    sub_category,
    ROUND(AVG(discount)*100, 2) AS avg_discount,
    ROUND(AVG(profit_margin_pct), 2) AS avg_margin,
    CASE
        WHEN AVG(discount) = 0           THEN 'No Discount'
        WHEN AVG(discount) <= 0.10       THEN 'Low Discount'
        WHEN AVG(discount) <= 0.20       THEN 'Medium Discount'
        ELSE 'High Discount'
    END AS discount_tier
FROM orders
GROUP BY sub_category
ORDER BY avg_discount DESC;


-- ============================================================
-- SECTION 5 — JOINS (Self-Join Pattern & Subquery Join)
-- ============================================================

-- Q15: Orders with above-average sales (using subquery join)
SELECT
    o.order_id,
    o.customer_name,
    o.category,
    o.sales,
    o.profit
FROM orders o
JOIN (
    SELECT AVG(sales) AS avg_sales FROM orders
) avg_tbl ON o.sales > avg_tbl.avg_sales
ORDER BY o.sales DESC
LIMIT 20;


-- ============================================================
-- SECTION 6 — SUBQUERIES
-- ============================================================

-- Q16: Customers who generated more profit than the average customer
SELECT customer_name, total_profit
FROM (
    SELECT customer_name, SUM(profit) AS total_profit
    FROM orders
    GROUP BY customer_name
) cust_profit
WHERE total_profit > (
    SELECT AVG(cust_avg.avg_profit)
    FROM (
        SELECT SUM(profit) AS avg_profit
        FROM orders
        GROUP BY customer_name
    ) cust_avg
)
ORDER BY total_profit DESC;

-- Q17: Most profitable product in each category (correlated subquery)
SELECT
    category,
    sub_category,
    product_name,
    total_profit
FROM (
    SELECT
        category,
        sub_category,
        product_name,
        SUM(profit) AS total_profit,
        RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS rnk
    FROM orders
    GROUP BY category, sub_category, product_name
) ranked
WHERE rnk = 1;


-- ============================================================
-- SECTION 7 — CTEs (Common Table Expressions)
-- ============================================================

-- Q18: Year-over-Year sales growth using CTE
WITH yearly_sales AS (
    SELECT
        year,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY year
),
yoy AS (
    SELECT
        curr.year,
        curr.total_sales,
        prev.total_sales AS prev_year_sales,
        ROUND((curr.total_sales - prev.total_sales) / prev.total_sales * 100, 2) AS yoy_growth_pct
    FROM yearly_sales curr
    LEFT JOIN yearly_sales prev ON curr.year = prev.year + 1
)
SELECT * FROM yoy ORDER BY year;

-- Q19: Customer Lifetime Value with tier classification
WITH customer_ltv AS (
    SELECT
        customer_id,
        customer_name,
        segment,
        SUM(sales)               AS lifetime_value,
        SUM(profit)              AS total_profit,
        COUNT(DISTINCT order_id) AS total_orders,
        MIN(order_date)          AS first_order,
        MAX(order_date)          AS last_order
    FROM orders
    GROUP BY customer_id, customer_name, segment
)
SELECT *,
    CASE
        WHEN lifetime_value >= 10000 THEN 'Platinum'
        WHEN lifetime_value >= 5000  THEN 'Gold'
        WHEN lifetime_value >= 1000  THEN 'Silver'
        ELSE 'Bronze'
    END AS customer_tier
FROM customer_ltv
ORDER BY lifetime_value DESC
LIMIT 30;


-- ============================================================
-- SECTION 8 — WINDOW FUNCTIONS
-- ============================================================

-- Q20: Running Total of Sales by Year
SELECT
    order_date,
    year,
    sales,
    SUM(sales) OVER (
        PARTITION BY year
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_sales
FROM orders
ORDER BY year, order_date
LIMIT 30;

-- Q21: Rank customers by total sales (RANK vs DENSE_RANK)
SELECT
    customer_name,
    segment,
    total_sales,
    RANK()       OVER (ORDER BY total_sales DESC) AS rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY total_sales DESC) AS dense_rank,
    ROW_NUMBER() OVER (ORDER BY total_sales DESC) AS row_num
FROM (
    SELECT customer_name, segment, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_name, segment
) t
LIMIT 20;

-- Q22: Monthly Moving Average of Sales (3-month)
WITH monthly AS (
    SELECT
        year,
        MONTH(order_date) AS month,
        SUM(sales)        AS monthly_sales
    FROM orders
    GROUP BY year, MONTH(order_date)
)
SELECT
    year,
    month,
    monthly_sales,
    ROUND(AVG(monthly_sales) OVER (
        ORDER BY year, month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3m
FROM monthly
ORDER BY year, month;

-- Q23: Sub-category profit rank within each category
SELECT
    category,
    sub_category,
    SUM(profit)                                             AS total_profit,
    RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS rank_in_category
FROM orders
GROUP BY category, sub_category
ORDER BY category, rank_in_category;


-- ============================================================
-- SECTION 9 — DATE FUNCTIONS
-- ============================================================

-- Q24: Sales by Quarter
SELECT
    year,
    QUARTER(order_date)     AS quarter,
    SUM(sales)              AS quarterly_sales,
    SUM(profit)             AS quarterly_profit
FROM orders
GROUP BY year, QUARTER(order_date)
ORDER BY year, quarter;

-- Q25: Month-over-month sales for the latest year
SELECT
    MONTHNAME(order_date)   AS month_name,
    MONTH(order_date)       AS month_num,
    SUM(sales)              AS monthly_sales
FROM orders
WHERE year = (SELECT MAX(year) FROM orders)
GROUP BY MONTHNAME(order_date), MONTH(order_date)
ORDER BY month_num;


-- ============================================================
-- SECTION 10 — VIEWS (Reusable Query Objects)
-- ============================================================

-- View 1: Executive KPI Summary (used in Power BI)
CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT
    year,
    SUM(sales)                              AS total_sales,
    SUM(profit)                             AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2)    AS profit_margin_pct,
    COUNT(DISTINCT order_id)               AS total_orders,
    COUNT(DISTINCT customer_id)            AS unique_customers,
    ROUND(SUM(sales)/COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM orders
GROUP BY year;

-- View 2: Product profitability view
CREATE OR REPLACE VIEW vw_product_profitability AS
SELECT
    product_id,
    product_name,
    category,
    sub_category,
    SUM(sales)                              AS total_sales,
    SUM(profit)                             AS total_profit,
    SUM(quantity)                           AS units_sold,
    ROUND(SUM(profit)/SUM(sales)*100, 2)    AS margin_pct,
    ROUND(AVG(discount)*100, 2)             AS avg_discount_pct
FROM orders
GROUP BY product_id, product_name, category, sub_category;

-- View 3: Customer 360 View
CREATE OR REPLACE VIEW vw_customer_360 AS
SELECT
    customer_id,
    customer_name,
    segment,
    region,
    market,
    SUM(sales)               AS lifetime_value,
    SUM(profit)              AS total_profit_contributed,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(discount)*100, 2) AS avg_discount_used,
    MIN(order_date)          AS first_purchase,
    MAX(order_date)          AS last_purchase
FROM orders
GROUP BY customer_id, customer_name, segment, region, market;

-- ============================================================
-- END OF SQL ANALYSIS FILE
-- ============================================================
