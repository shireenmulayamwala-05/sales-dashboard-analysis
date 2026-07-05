# Resume Bullet Points & Interview Preparation
## E-Commerce Sales & Customer Analytics Project

---

## ATS-Friendly Resume Bullet Points

Use these on your resume under a "Projects" section.
Pick 3–4 that are most relevant to the job you're applying for.

---

**E-Commerce Sales & Customer Analytics Dashboard**  
*Python | SQL | Power BI | Pandas | MySQL | Matplotlib*

- Analysed 51,290 e-commerce transactions across 7 global markets using Python (Pandas) to identify discount-driven profit losses totalling negative margin in 3 product sub-categories
- Wrote 25 SQL queries ranging from basic aggregation to advanced window functions (RANK, DENSE_RANK, running totals, 3-month moving averages) to extract business KPIs for executive reporting
- Identified that orders with discounts above 20% consistently result in negative profit margins, leading to a recommendation to cap Furniture discounts at 10%
- Built a 5-page interactive Power BI dashboard with DAX measures, slicers, drill-through, and conditional formatting to enable self-service analytics for Sales, Finance, and Marketing teams
- Performed customer segmentation analysis revealing that the top 20% of customers generate approximately 80% of total revenue, informing a VIP loyalty programme recommendation
- Engineered derived features including profit margin %, shipping days, and discount brackets to support both SQL views and Power BI DAX measures

---

## Interview Questions & Model Answers

---

### SQL Questions

**Q: What is the difference between WHERE and HAVING?**

WHERE filters rows before aggregation.  
HAVING filters groups after aggregation.

Example: If you want customers who spent more than $5,000 total, you cannot use WHERE because the total doesn't exist at the row level. You use GROUP BY + HAVING.

```sql
SELECT customer_name, SUM(sales) AS total
FROM orders
GROUP BY customer_name
HAVING total > 5000;
```

---

**Q: What is the difference between RANK, DENSE_RANK, and ROW_NUMBER?**

All three rank rows. The difference is how they handle ties:
- ROW_NUMBER: always unique, no ties (1, 2, 3, 4)
- RANK: skips numbers after ties (1, 2, 2, 4)
- DENSE_RANK: no gaps after ties (1, 2, 2, 3)

Use RANK for "top N" lists where ties matter.  
Use ROW_NUMBER for pagination or when you need a unique identifier.

---

**Q: What is a CTE and when would you use it over a subquery?**

A CTE (Common Table Expression) is a named temporary result set defined with WITH.

Use a CTE when:
- The subquery is used more than once in the same query
- The logic is complex and you want to make it readable
- You need to build logic step by step (chained CTEs)

CTEs don't improve performance — they improve readability and maintainability.

---

**Q: What is a window function?**

A window function performs a calculation across a set of rows related to the current row, without collapsing the result into a single row (unlike GROUP BY).

Example: Running total of sales — you want each row to still show order-level detail, but also include the cumulative total up to that point.

```sql
SUM(sales) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

---

### Python Questions

**Q: What is the difference between loc and iloc in Pandas?**

- `loc` selects by label (column name or index label)
- `iloc` selects by integer position (0, 1, 2...)

Example:
```python
df.loc[0, "sales"]       # row label 0, column named "sales"
df.iloc[0, 5]            # row position 0, column position 5
```

---

**Q: How did you handle missing values in this project?**

First I identified them using `df.isnull().sum()`. In this dataset there were no significant missing values. But the standard approach is:
- For numerical columns: fill with median (not mean — median is robust to outliers)
- For categorical columns: fill with mode or a placeholder like "Unknown"
- For date columns: investigate why they are missing before filling

Never drop rows blindly — understand why the data is missing first.

---

**Q: What is feature engineering? Give an example from your project.**

Feature engineering is creating new columns from existing data to make analysis more meaningful.

Examples from this project:
- `shipping_days` = ship_date minus order_date — measures operational efficiency
- `profit_margin_pct` = (profit / sales) × 100 — normalises profit for fair comparison
- `discount_bracket` = categorised discount into bands (No Discount, 1–10%, etc.) — enables segmentation

Without these derived columns, the analysis would be limited to raw numbers.

---

### Business / Case Questions

**Q: You find that one region has high sales but low profit. What do you do?**

1. First confirm the numbers — is it a data quality issue or a real trend?
2. Drill down: is it one category, one sub-category, or across the board?
3. Check discount rates for that region specifically
4. Check shipping costs — are they unusually high?
5. Look at the product mix — are they selling more low-margin items?
6. Present findings to Sales and Finance with 2–3 specific recommendations

I would not jump to conclusions — I would follow the data trail.

---

**Q: How would you explain the Pareto principle to a non-technical manager?**

I would say: "About 20% of your customers are responsible for roughly 80% of your revenue. This means if we lose even 10 of our top customers, we could see a significant drop in revenue. The recommendation is to identify those customers, treat them as VIPs, and build a retention strategy specifically for them."

---

**Q: A manager asks you 'why are profits dropping?' — how do you structure your answer?**

I would structure it as: Diagnosis → Evidence → Recommendation.

1. "I looked at profit by year and confirmed the drop is real — margins fell from X% to Y%."
2. "Drilling into categories, Furniture shows negative profit driven by discounts above 30%."
3. "My recommendation is to cap Furniture discounts at 10% and run a 90-day test to see if volume holds."

Always lead with data, not opinion.

---

### Behavioural Questions

**Q: Tell me about a time you found an unexpected insight in data.**

"In this project I expected discounts to uniformly hurt margins, but the data showed that small discounts (1–10%) actually had healthy profit margins — close to or better than no-discount orders. The real damage came specifically from discounts above 20%. That nuance changed my recommendation from 'eliminate discounts' to 'cap discounts at 15%' — which is a much more actionable and realistic business recommendation."

---

**Q: How do you communicate findings to non-technical stakeholders?**

I focus on business impact, not technical details. Instead of saying "the correlation between discount and profit is -0.48", I say "for every 10% increase in discount, profit margin drops by about 5 percentage points — and above 20% discount we are typically selling at a loss."

Numbers with context land better than numbers alone.

---

*Practice answering these out loud. The goal is fluency, not memorisation.*
