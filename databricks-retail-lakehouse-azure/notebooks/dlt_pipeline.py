# Databricks notebook source
# Delta Live Tables pipeline
import dlt
from pyspark.sql.functions import col, explode, to_timestamp

CAT = "retail_prod"
SCH = "core"
RAW = f"/Volumes/{CAT}/{SCH}/raw/orders"

@dlt.view(name="orders_raw", comment="Raw orders from UC Volume or ABFSS")
def orders_raw():
    return (spark.readStream.format("cloudFiles")
            .option("cloudFiles.format","json")
            .option("cloudFiles.schemaLocation", f"/Volumes/{CAT}/{SCH}/_checkpoints/dlt_schema")
            .load(RAW))

@dlt.table(comment="Bronze orders with minimal validation")
@dlt.expect("non_null_keys", "order_id IS NOT NULL AND customer_id IS NOT NULL")
def orders_bronze():
    return dlt.read_stream("orders_raw").withColumn("_ingest_ts", to_timestamp("_metadata.file_modification_time"))

@dlt.table(comment="Silver orders header")
def orders_silver():
    return dlt.read("orders_bronze").withColumn("order_ts", to_timestamp("order_ts"))

@dlt.table(comment="Silver order lines")
def order_lines_silver():
    return (dlt.read("orders_silver")
            .withColumn("item", explode("items"))
            .select("order_id","customer_id","order_ts","store_id",
                    col("item.sku").alias("sku"), col("item.qty").alias("qty"), col("item.price").alias("price"))
            .withColumn("extended_price", col("qty")*col("price")))

@dlt.table(comment="Gold: daily revenue per store")
def fact_daily_store_revenue_gold():
    return spark.sql(f'''
        SELECT date_trunc('day', o.order_ts) AS order_date, o.store_id,
               SUM(l.extended_price) AS gross_revenue, COUNT(DISTINCT o.order_id) AS orders
        FROM LIVE.orders_silver o
        JOIN LIVE.order_lines_silver l USING (order_id)
        GROUP BY 1,2
    ''')
