-- Basic Unity Catalog grants (example)
GRANT USAGE ON CATALOG retail_prod TO `bi_analysts`;
GRANT USAGE ON SCHEMA retail_prod.core TO `bi_analysts`;
GRANT SELECT ON TABLE retail_prod.core.fact_daily_store_revenue_gold TO `bi_analysts`;
