# Databricks notebook source
# COMMAND ----------
from pyspark.sql.functions import current_timestamp

CAT = dbutils.widgets.get("cat") if "cat" in [w.name for w in dbutils.widgets.get()] else "retail_prod"
SCH = dbutils.widgets.get("sch") if "sch" in [w.name for w in dbutils.widgets.get()] else "core"
dbutils.widgets.text("cat", CAT); dbutils.widgets.text("sch", SCH)
spark.sql(f"USE CATALOG {CAT}"); spark.sql(f"USE {SCH}")

RAW = f"/Volumes/{CAT}/{SCH}/raw/orders"   # or ABFSS path
BRONZE_TBL = f"{CAT}.{SCH}.orders_bronze"
CHK = f"/Volumes/{CAT}/{SCH}/_checkpoints/orders_bronze"

bronze_df = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format","json")
    .option("cloudFiles.schemaLocation", CHK + "/schema")
    .load(RAW)
    .withColumn("_ingest_ts", current_timestamp())
)

(
  bronze_df.writeStream
    .format("delta")
    .option("checkpointLocation", CHK)
    .outputMode("append")
    .trigger(once=True)
    .toTable(BRONZE_TBL)
)
