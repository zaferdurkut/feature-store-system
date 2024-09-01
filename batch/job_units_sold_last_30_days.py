from datetime import datetime, timedelta

import redis
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, to_date, sum
from pyspark.sql.types import IntegerType

# spark-submit --master spark://spark:7077 /opt/batch/job_units_sold_last_30_days.py

# Initialize Spark session with Hive support
spark = SparkSession.builder \
    .appName("UnitsSoldLast30Days") \
    .enableHiveSupport() \
    .config("spark.sql.warehouse.dir", "/stream/hive/warehouse") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .getOrCreate()

print("UnitsSoldLast30Days spark session started")
# Connect to Redis
redis_client = redis.Redis(host='batch-redis', port=6379, db=0)


# Load the data from Hive
df = spark.sql("SELECT ProductID, Quantity, TransactionDate FROM testdb.ecommerce_transactions")

df = df.filter(
    col("ProductID").isNotNull() &
    col("Quantity").isNotNull() &
    col("TransactionDate").isNotNull()
)

# Convert TransactionDate
df = df.withColumn("TransactionDate", to_date(col("TransactionDate")))

# Handle non-numeric values in Quantity
df = df.withColumn(
    "Quantity",
    when(col("Quantity").cast(IntegerType()).isNotNull(), col("Quantity").cast(IntegerType())).otherwise(0)
)

# Filter data for the last 30 days
current_date = datetime.now().date()
thirty_days_ago = current_date - timedelta(days=30)
df_filtered = df.filter(col("TransactionDate").between(thirty_days_ago, current_date))

# Calculate the number of units sold per ProductID
units_sold_df = df_filtered.groupBy("ProductID").agg(sum("Quantity").alias("UnitsSold"))

# units_sold_df.show()

# Write the result to Redis
for row in units_sold_df.collect():
    product_id = row["ProductID"]
    units_sold = row["UnitsSold"]
    redis_client.set(f"units_sold:{product_id}", units_sold)

# Use foreachPartition to process each partition separately
# avg_reviews_df.foreachPartition(write_to_redis)

print("Units sold per product for the last 30 days has been written to Redis")
# Stop Spark session
spark.stop()
