# Databricks 'Vibe' Notebook for Azure
# One notebook to ingest -> silver -> gold with synthetic data

# COMMAND ----------
# Setup widgets & paths
from pyspark.sql import functions as F
import json, random, time
from datetime import datetime, timedelta

CAT = dbutils.widgets.get("cat") if "cat" in [w.name for w in dbutils.widgets.get()] else "playground"
SCH = dbutils.widgets.get("sch") if "sch" in [w.name for w in dbutils.widgets.get()] else "core"
dbutils.widgets.text("cat", CAT); dbutils.widgets.text("sch", SCH)
spark.sql(f"USE CATALOG {CAT}"); spark.sql(f"USE {SCH}")
spark.conf.set("spark.sql.shuffle.partitions", 64)

# Try a managed UC Volume first, fallback to ABFSS
RAW = f"/Volumes/{CAT}/{SCH}/v_raw/orders"
try:
    dbutils.fs.mkdirs(RAW)
except Exception:
    RAW = "abfss://datalake@<ACCOUNT>.dfs.core.windows.net/retail/raw/orders"

BRONZE=f"{CAT}.{SCH}.orders_bronze"
SILVER_ORD=f"{CAT}.{SCH}.orders_silver"
SILVER_LINE=f"{CAT}.{SCH}.order_lines_silver"
GOLD_FACT=f"{CAT}.{SCH}.fact_daily_store_revenue_gold"

# COMMAND ----------
# Generate synthetic JSON orders
now = datetime.utcnow()
dbutils.fs.mkdirs(RAW)
path=f"{RAW}/batch_{int(time.time())}.json"
lines = []
for i in range(1,501):
    lines.append(json.dumps({
      "order_id": i,
      "customer_id": random.randint(100,199),
      "order_ts": (now - timedelta(minutes=random.randint(0,240))).isoformat()+"Z",
      "status": random.choice(["PAID","PAID","SHIPPED","CANCELLED"]),
      "currency": "USD",
      "store_id": random.randint(1,5),
      "items": [{"sku": f"S{random.randint(10,19)}", "qty": random.randint(1,3), "price": round(random.uniform(5,30),2)}]
    }))
dbutils.fs.put(path, "\n".join(lines), overwrite=True)
display(dbutils.fs.ls(RAW))

# COMMAND ----------
# Bronze (Auto Loader, run-once)
from pyspark.sql.functions import current_timestamp
CHK=f"/Volumes/{CAT}/{SCH}/_checkpoints/orders_bronze"
bronze_df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format","json")
    .option("cloudFiles.schemaLocation", CHK + "/schema")
    .load(RAW)
    .withColumn("_ingest_ts", current_timestamp()))
(bronze_df.writeStream
 .format("delta")
 .option("checkpointLocation", CHK)
 .trigger(once=True)
 .toTable(BRONZE))

# COMMAND ----------
# Silver (clean + explode)
from pyspark.sql.functions import col, explode, to_timestamp, when
bronze = spark.table(BRONZE)
orders = (bronze
  .withColumn("order_ts", to_timestamp("order_ts"))
  .withColumn("status", when(col("status").isin("PAID","SHIPPED","CANCELLED"), col("status")).otherwise("UNKNOWN"))
)
lines = (orders
  .withColumn("item", explode("items"))
  .select("order_id","customer_id","order_ts","store_id",
          col("item.sku").alias("sku"), col("item.qty").alias("qty"), col("item.price").alias("price"))
  .withColumn("extended_price", col("qty")*col("price"))
)
orders.write.mode("overwrite").saveAsTable(SILVER_ORD)
lines.write.mode("overwrite").saveAsTable(SILVER_LINE)

# COMMAND ----------
# Gold
spark.sql(f'''
CREATE OR REPLACE TABLE {GOLD_FACT} AS
SELECT date_trunc('day', o.order_ts) AS order_date,
       o.store_id,
       SUM(l.extended_price) AS gross_revenue,
       COUNT(DISTINCT o.order_id) AS orders
FROM {SILVER_ORD} o
JOIN {SILVER_LINE} l USING (order_id)
GROUP BY 1,2
''')
display(spark.table(GOLD_FACT).orderBy(F.col("order_date").desc(), F.col("store_id")))
