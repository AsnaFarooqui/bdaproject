from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, explode, count, sum as _sum,
    avg, to_timestamp, window, date_format, concat_ws
)

# -----------------------------------
# Spark Session with Mongo Connector
# -----------------------------------
spark = SparkSession.builder \
    .appName("Mongo-KPI-Aggregation") \
    .config("spark.mongodb.input.uri", "mongodb://mongo:27017/bda_project.orders_stream") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/bda_project.kpi_minute") \
    .getOrCreate()

# -----------------------------------
# Read raw orders from Mongo
# -----------------------------------
orders = spark.read.format("com.mongodb.spark.sql.DefaultSource") \
    .option("uri", "mongodb://mongo:27017/bda_project.orders_stream") \
    .load()

# -----------------------------------
# Explode items (nested schema)
# -----------------------------------
orders_items = orders.withColumn(
    "item", explode("items")
)

# -----------------------------------
# Convert timestamp
# -----------------------------------
orders_items = orders_items.withColumn(
    "event_time", to_timestamp("timestamp")
)

# -----------------------------------
# KPI Aggregation (per minute)
# -----------------------------------
kpi_df = orders_items.groupBy(
    window(col("event_time"), "1 minute"),
    col("customer_state"),
    col("item.product_category")
).agg(
    count("order_id").alias("total_orders"),
    _sum("payment_value").alias("total_sales"),
    _sum("item.quantity").alias("total_items"),
    avg("payment_value").alias("avg_order_value")
)

# -----------------------------------
# Flatten window
# -----------------------------------
final_df = kpi_df.select(
    col("window.start").alias("minute"),
    col("customer_state"),
    col("product_category"),
    col("total_orders"),
    col("total_sales"),
    col("total_items"),
    col("avg_order_value"),
    concat_ws(
        "-",
        date_format(col("window.start"), "yyyy-MM-dd-HH-mm"),
        col("customer_state"),
        col("product_category")
    ).alias("_id")
)


# -----------------------------------
# Write KPIs back to Mongo
# -----------------------------------

(
    final_df.write
        .format("com.mongodb.spark.sql.DefaultSource")
        .mode("append")
        .option("uri", "mongodb://mongo:27017/bda_project.kpi_minute")
        .option("replaceDocument", "true")
        .save()
)

spark.stop()

