from datetime import datetime, timedelta

import redis
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, to_date, sum
from pyspark.sql.types import IntegerType, FloatType

# spark-submit --master spark://spark:7077 /opt/batch/job_revenue_by_category_last_30_days.py

# Initialize Spark session with Hive support
spark = SparkSession.builder \
    .appName("RevenueByCategoryLast30Days") \
    .enableHiveSupport() \
    .config("spark.sql.warehouse.dir", "/stream/hive/warehouse") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .getOrCreate()

print("RevenueByCategoryLast30Days spark session started")
# Connect to Redis
redis_client = redis.Redis(host='batch-redis', port=6379, db=0)



# Load the data from Hive
df = spark.sql("SELECT Category, Price, Quantity, TransactionDate FROM testdb.ecommerce_transactions")

# Filter out rows where any of the critical fields are None
df = df.filter(
    col("Category").isNotNull() &
    col("Price").isNotNull() &
    col("Quantity").isNotNull() &
    col("TransactionDate").isNotNull()
)

# Handle non-numeric values in Quantity and Price
df = df.withColumn(
    "Quantity",
    when(col("Quantity").cast(IntegerType()).isNotNull(), col("Quantity").cast(IntegerType())).otherwise(0)
)

df = df.withColumn(
    "Price",
    when(col("Price").cast(FloatType()).isNotNull(), col("Price").cast(FloatType())).otherwise(0.0)
)

# Convert TransactionDate to date type if not already
df = df.withColumn("TransactionDate", to_date(col("TransactionDate")))

# Filter data for the last 30 days
current_date = datetime.now().date()
thirty_days_ago = current_date - timedelta(days=30)
df_filtered = df.filter(col("TransactionDate").between(thirty_days_ago, current_date))

# Calculate revenue (Price * Quantity)
df_filtered = df_filtered.withColumn("Revenue", col("Price") * col("Quantity"))

# Calculate the total revenue per Category
revenue_df = df_filtered.groupBy("Category").agg(sum("Revenue").alias("TotalRevenue"))


# units_sold_df.show()

# Write the result to Redis
for row in revenue_df.collect():
    category = row["Category"]
    total_revenue = row["TotalRevenue"]
    redis_key = f"revenue_by_category:{category}"
    redis_client.set(redis_key, total_revenue)

# Use foreachPartition to process each partition separately
# avg_reviews_df.foreachPartition(write_to_redis)

print("Revenue by category for the last 30 days has been written to Redis")
# Stop Spark session
spark.stop()
