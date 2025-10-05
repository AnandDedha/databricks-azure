import pyspark.sql.functions as F
from chispa import assert_df_equality

def test_extended_price(spark):
    input_df = spark.createDataFrame([(2, 10.0)], ["qty","price"])
    actual = input_df.withColumn("extended_price", F.col("qty") * F.col("price"))
    expected = spark.createDataFrame([(2,10.0,20.0)], ["qty","price","extended_price"])
    assert_df_equality(actual, expected, ignore_row_order=True, ignore_column_order=True)
