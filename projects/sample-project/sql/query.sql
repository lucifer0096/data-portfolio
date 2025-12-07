-- Example SQL: monthly sales totals
-- Replace table_name with your table or use this as a template for local SQLite/DB
SELECT
  strftime('%Y-%m', date) AS year_month,
  SUM(sales) AS total_sales
FROM sales_table
GROUP BY year_month
ORDER BY year_month;
