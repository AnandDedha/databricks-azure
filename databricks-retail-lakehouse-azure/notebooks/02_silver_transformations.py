# Databricks notebook source
# COMMAND ----------
from pyspark.sql.functions import col, explode, to_timestamp, when

CAT = dbutils.widgets.get("cat") if "cat" in [w.name for w in dbutils.widgets.get()] else "retail_prod"
SCH = dbutils.widgets.get("sch") if "sch" in [w.name for w in dbutils.widgets.get()] else "core"
dbutils.widgets.text("cat", CAT); dbutils.widgets.text("sch", SCH)
spark.sql(f"USE CATALOG {CAT}"); spark.sql(f"USE {SCH}")

BRONZE_TBL = f"{CAT}.{SCH}.orders_bronze"

orders = (
  spark.table(BRONZE_TBL)
  .withColumn("order_ts", to_timestamp("order_ts"))
  .withColumn("status", when(col("status").isin("PAID","SHIPPED","CANCELLED"), col("status")).otherwise("UNKNOWN"))
)

lines = (
  orders
  .withColumn("item", explode("items"))
  .select("order_id","customer_id","order_ts","store_id",
          col("item.sku").alias("sku"),
          col("item.qty").alias("qty"),
          col("item.price").alias("price"))
  .withColumn("extended_price", col("qty")*col("price"))
)

orders.write.mode("overwrite").saveAsTable(f"{CAT}.{SCH}.orders_silver")
lines.write.mode("overwrite").saveAsTable(f"{CAT}.{SCH}.order_lines_silver")
