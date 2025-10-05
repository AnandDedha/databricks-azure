-- Databricks SQL notebook
-- Daily revenue per store (Gold)
CREATE OR REPLACE TABLE ${cat}.${sch}.fact_daily_store_revenue_gold AS
SELECT
  date_trunc('day', o.order_ts) AS order_date,
  o.store_id,
  SUM(l.extended_price) AS gross_revenue,
  COUNT(DISTINCT o.order_id) AS orders
FROM ${cat}.${sch}.orders_silver o
JOIN ${cat}.${sch}.order_lines_silver l USING (order_id)
GROUP BY 1,2;

-- Example query
SELECT * FROM ${cat}.${sch}.fact_daily_store_revenue_gold ORDER BY order_date DESC, store_id;
